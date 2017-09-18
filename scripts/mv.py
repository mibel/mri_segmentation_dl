import os
from os.path import join as op_join
from shutil import copyfile


WMH_ORIG = '/home/mikhail/nhw/data/wmh'
WMH_PREPROC = '/home/mikhail/nhw/data/derivatives/datasink/preproc'

if __name__ == "__main__":
    cites = os.listdir(WMH_ORIG)
    fnames_to_copy = ['brainmask_T1_mask.nii.gz', 'FLAIR.nii.gz', 'T1.nii.gz']
    for cite in cites:
        cite_root = op_join(WMH_ORIG, cite)
        tom = os.listdir(cite_root)[0]
        tom_root = op_join(cite_root, tom)
        for subj in os.listdir(tom_root):
            dest_root = op_join(WMH_PREPROC, 'sub-{}{}'.format(cite, subj))
            src_root = op_join(tom_root, subj)
            copyfile(op_join(src_root, 'wmh.nii.gz'),
                     op_join(dest_root, 'lesion_mask_flair.nii.gz'))
            for fname in fnames_to_copy:
                copyfile(op_join(src_root, 'pre', fname),
                         op_join(dest_root, fname))
