import os
from os.path import join as op_join
import pandas as pd

FNAMES_MAP = {
    'FLAIR.nii.gz': 'flair_flairspace',
    'T1.nii.gz': 't1_flairspace',
    'lesion_mask_flair.nii.gz': 'target_flairspace',
    'brainmask_T1_mask.nii.gz': 'brainmask_flairspace',
    'FLAIR_warped.nii.gz': 'flair',
    'T1w_base.nii.gz': 't1',
    'lesion_mask_t1.nii.gz': 'target',
    'T1w_brain_mask.nii.gz': 'brainmask',
    'FLAIR_warped_bias_corrected_fs_nucorrect.nii.gz': 'flair_fsn3',
    'FLAIR_warped_bias_corrected_ants_n4.nii.gz': 'flair_antsn3',
    'T1w_bias_corrected_fs_nucorrect.nii.gz': 't1_fsn3',
    'T1w_bias_corrected_ants_n4.nii.gz': 't1_antsn3',
    'T1w_bias_corrected_ants_n4_labeled.nii.gz': 't1_wm_mask',
}
ROOT_DIR = '/home/mikhail/nhw/data/derivatives/datasink/preproc'

if __name__ == "__main__":
    subjects = [f for f in os.listdir(ROOT_DIR)
                if os.path.isdir(op_join(ROOT_DIR, f))]
    df = pd.DataFrame(data=None, index=subjects,
                      columns=list(FNAMES_MAP.values()) + ['cite'])
    for subj in subjects:
        for fname in list(FNAMES_MAP.keys()):
            df.loc[subj, FNAMES_MAP[fname]] = op_join(subj, fname)
        subj_id = subj.split('-')[1]
        df.loc[subj, 'cite'] = ''.join(i for i in subj_id if not i.isdigit())
    df.to_csv(op_join(ROOT_DIR, 'metadata.csv'), index_label='id')
