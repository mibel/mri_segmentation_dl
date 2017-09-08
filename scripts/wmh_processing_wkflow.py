# coding: utf-8
import os
from os.path import join as opj

import nipype.interfaces.fsl.preprocess as ni_fsl_preproc
import nipype.interfaces.ants as ni_ants
import nipype.interfaces.freesurfer as ni_fs
import nipype.interfaces.afni as ni_afni
import nipype.interfaces.utility as ni_util # IdentityInterface
import nipype.interfaces.io as ni_io # SelectFiles, DataSink
import nipype.pipeline.engine as ni_engine # Workflow, Node

DEBUG = True
DATA_ROOT = '/data'
experiment_dir = opj(DATA_ROOT, 'derivatives')
output_dir = 'datasink'
working_dir = 'wd'


# ANTs: Rigid registration of T1 to FLAIR
# TODO: Bias correct T1 and FLAIR before registration
ants_reg = ni_engine.Node(ni_ants.Registration(dimension=3,
                                               transforms=['Rigid'],
                                               transform_parameters=[(0.1,)],
                                               metric=['MI'],
                                               metric_weight=[1.0],
                                               number_of_iterations=[[1000]],
                                               convergence_threshold=[1.e-7],
                                               convergence_window_size=[10],
                                               shrink_factors=[[4]],
                                               smoothing_sigmas=[[2.]],
                                               output_warped_image=True,
                                               output_transform_prefix='T1w_to_FLAIR'),
                         name='ants_reg')

# BET: skullstrip T1
bet_t1 = ni_engine.Node(ni_fsl_preproc.BET(frac=0.2,
                                           robust=True,
                                           output_type='NIFTI_GZ',
                                           mask=True),
                        name="bet_t1")

ants_warp_lesion = ni_engine.Node(ni_ants.ApplyTransforms(dimension=3,
                                                     interpolation='NearestNeighbor',
                                                     invert_transform_flags=[True],
                                                          default_value=0),
                                  name='ants_warp_lesion')

ants_warp_flair = ni_engine.Node(ni_ants.ApplyTransforms(dimension=3,
                                                     interpolation='NearestNeighbor',
                                                     invert_transform_flags=[True],
                                                          default_value=0),
                                  name='ants_warp_flair')

bias_correct_t1_fs_nucorrect = ni_engine.Node(ni_fs.MNIBiasCorrection(),
                                             name='bias_correct_t1_fs_nucorrect')
bias_correct_t1_ants_n4 = ni_engine.Node(ni_ants.N4BiasFieldCorrection(),
                                        name='bias_correct_t1_ants_n4')
segment_t1_ants_atropos = ni_engine.Node(ni_ants.Atropos(number_of_tissue_classes=3,
                                                        initialization='KMeans',
                                                        save_posteriors=True),
                                        name='segment_t1_ants_atropos')

# TODO: Break out masking as separate workflow?
# TODO: Separate WM mask
# TODO: Binarize WM mask (may not be strictly necessary)
# TODO: Mask T1 with WM mask
# TODO: Mask FLAIR with WM mask

copy_t1 = ni_engine.Node(ni_afni.Copy(outputtype='NIFTI_GZ'),
                        name='copy_t1')


# Manually defined lists for now
site_top_list = ('Amst',)
site_bot_list = ('GE3T',)

if DEBUG is True:
    sub_list = ('100',)
else: 
    sub_list = ('100', '101', '102')


# Infosource
infosource = ni_engine.Node(ni_util.IdentityInterface(fields=['site_top', 'site_bot', 'subject_id']),
                  name="infosource")
infosource.iterables = [('site_top', site_top_list),
                        ('site_bot', site_bot_list),
                        ('subject_id', sub_list)]

# SelectFiles
t1_file = opj('wmh', '{site_top}', '{site_bot}', '{subject_id}', 'orig', '3DT1.nii.gz')
t1_mask = opj('wmh', '{site_top}', '{site_bot}', '{subject_id}', 'orig', '3DT1_mask.nii.gz')
t1_file_alt = opj('wmh', '{site_top}', '{site_bot}', '{subject_id}', 'orig', 'T1.nii.gz')
t1_alt_mask = opj('wmh', '{site_top}', '{site_bot}', '{subject_id}', 'orig', 'T1_mask.nii.gz')
flair_file = opj('wmh', '{site_top}', '{site_bot}',
                 '{subject_id}', 'orig', 'FLAIR.nii.gz')
lesion_file = opj('wmh', '{site_top}', '{site_bot}',
                  '{subject_id}', 'wmh.nii.gz')

templates = {'t1': t1_file,
             't1_mask': t1_mask,
             't1_alt': t1_file_alt,
             't1_alt_mask': t1_alt_mask,
             'flair': flair_file,
             'lesion': lesion_file}
selectfiles = ni_engine.Node(ni_io.SelectFiles(templates,
                                               base_directory=DATA_ROOT,
                                               sort_filelist=True),
                             name="selectfiles")
                            
# Datasink - creates output folder for important outputs
ds_resubs = [(r'_site_bot_(?P<site_bot>.*)_site_top_(?P<site_top>.*)_subject_id_(?P<subject_id>\d+)',
              r'sub-\g<site_top>\g<subject_id>'),
             (r'3DT1\.nii\.gz', r'T1w_base.nii.gz'),
             (r'3DT1', r'T1w'),
             (r'_corrected', '_bias_corrected_ants_n4'),
             (r'_output', '_bias_corrected_fs_nucorrect'),
             (r'wmh_trans', r'lesion_mask_t1'),
             ('_copy', '_base')
            ]
datasink = ni_engine.Node(ni_io.DataSink(base_directory=experiment_dir,
                                         container=output_dir,
                                         regexp_substitutions=ds_resubs),
                          name="datasink")


# Create the preprocessing workflow
preproc = ni_engine.Workflow(name='preproc')
preproc.base_dir = opj(experiment_dir, working_dir)

# Connect all components of the preprocessing workflow
preproc.connect([(infosource, selectfiles, [('site_top', 'site_top'),
                                            ('site_bot', 'site_bot'),
                                            ('subject_id', 'subject_id')]),
                 (selectfiles, copy_t1, [('t1', 'in_file')]),
                 (selectfiles, bet_t1, [('t1', 'in_file')]),
                 (selectfiles, bias_correct_t1_ants_n4, [('t1', 'input_image')]),
                 (bet_t1, bias_correct_t1_ants_n4, [('mask_file', 'mask_image')]),                 
                 (selectfiles, bias_correct_t1_fs_nucorrect, [('t1', 'in_file')]),
                 (bet_t1, bias_correct_t1_fs_nucorrect, [('mask_file', 'mask')]),                 
                 (selectfiles, ants_reg, [('t1', 'moving_image'),
                                          ('t1_alt', 'fixed_image'),
                                          ('t1_mask', 'moving_image_mask'),
                                          ('t1_alt_mask', 'fixed_image_mask')]),
                 (ants_reg, ants_warp_lesion, [('reverse_transforms', 'transforms')]),
                 (selectfiles, ants_warp_lesion, [('t1', 'reference_image'),
                                           ('lesion', 'input_image')]),
                 (ants_reg, ants_warp_flair, [('reverse_transforms', 'transforms')]),
                 (selectfiles, ants_warp_flair, [('t1', 'reference_image'),
                                           ('flair', 'input_image')]),
                 (bias_correct_t1_ants_n4, segment_t1_ants_atropos, [('output_image', 'intensity_images')]),
                 (bet_t1, segment_t1_ants_atropos, [('mask_file', 'mask_image')]),                 
                 (bet_t1, datasink, [('out_file', 'preproc'),
                                     ('mask_file', 'preproc.@mask')]),
                 (ants_reg, datasink, [('composite_transform', 'preproc.@t1_to_flair_tf'),
                                       ('inverse_composite_transform', 'preproc.@flair_to_t1_tf')]),
                 (ants_warp_lesion, datasink, [('output_image', 'preproc.@lesion_to_t1_nii')]),
                 (ants_warp_flair, datasink, [('output_image', 'preproc.@flair_to_t1_nii')]),
                 (bias_correct_t1_ants_n4, datasink, [('output_image', 'preproc.@bc_ants_n4_t1')]),
                 (segment_t1_ants_atropos, datasink, [('classified_image', 'preproc.@seg_ants_atropos_t1')]),
                 (bias_correct_t1_fs_nucorrect, datasink, [('out_file', 'preproc.@bc_nucorrect_t1')]),
                 (copy_t1, datasink, [('out_file', 'preproc.@t1_base')]),
                 ])


wk_run = preproc.run('MultiProc', plugin_args={'n_procs': 4})
