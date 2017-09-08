import os
from os.path import join as op_join
import pandas as pd

FNAMES_MAP = {
    'brainmask_T1_mask.nii.gz': 'mask_flairspace',
    'FLAIR.nii.gz': 'flair_flairspace',
    'T1.nii.gz': 't1_flairspace',
    'lesion_mask_flair.nii.gz': 'target_flairspace',
    'FLAIR_trans.nii.gz': 'flair',
    'T1w_base.nii.gz': 't1',
    'lesion_mask_t1.nii.gz': 'target',
    # 'T1w_brain.nii.gz',
    'T1w_brain_mask.nii.gz': 'mask',
    'T1w_bias_corrected_fs_nucorrect.nii.gz': 't1_fsn3',
    'T1w_bias_corrected_ants_n4.nii.gz': 't1_antsn3',
    'T1w_bias_corrected_ants_n4_labeled.nii.gz': 't1_segm',
}
ROOT_DIR = '/home/mibel/wmh_preproc'

if __name__ == "__main__":
    subjects = [f for f in os.listdir(ROOT_DIR)
                if os.path.isdir(op_join(ROOT_DIR, f))]
    df = pd.DataFrame(data=None, index=subjects,
                      columns=list(FNAMES_MAP.values()) + ['group'])
    for subj in subjects:
        for fname in list(FNAMES_MAP.keys()):
            df.loc[subj, FNAMES_MAP[fname]] = op_join(subj, fname)
        subj_id = subj.split('-')[1]
        df.loc[subj, 'group'] = ''.join(i for i in subj_id if not i.isdigit())
    df.to_csv(op_join(ROOT_DIR, 'metadata.csv'), index_label='id')
