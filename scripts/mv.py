# list of files
# pre
#   - brainmask_T1_mask.nii.gz
#   - FLAIR.nii.gz
#   - T1.nii.gz
# FLAIR_trans.nii.gz
# T1w_bias_corrected_ants_n4_labeled.nii.gz
# T1w_brain_mask.nii.gz
# lesion_mask_t1.nii.gz
# T1w_bias_corrected_ants_n4.nii.gz
# T1w_brain.nii.gz
# T1w_base.nii.gz
# T1w_bias_corrected_fs_nucorrect.nii.gz

import os
from os.path import join as op_join
from shutil import copyfile


WMH_ORIG = '/home/mibel/wmh'
WMH_PREPROC = '/home/mibel/wmh_preproc'

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
