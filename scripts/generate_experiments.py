from dpipe.config import get_config, get_resource_manager
import json
from copy import deepcopy
import os.path as op
import os

CONFIG_PATH = 'configs'


def get_module_parent_dir():
    path = op.split(op.dirname(op.realpath(__file__)))[0]
    return path


def get_config_dir():
    dirname_full = op.join(get_module_parent_dir(), CONFIG_PATH)
    if not op.isdir(dirname_full):
        os.mkdir(dirname_full)
    return dirname_full


def fill_config(base_config, *, modalities, target):
    config = deepcopy(base_config)
    params = config['dataset_plain']['params']
    params['modalities'] = modalities
    params['target'] = target
    # remove apply_mask wrapper
    if len(modalities) == 2:
        config['dataset_masked'] = deepcopy(config['dataset_plain'])
    return config


def build_experiment(config, name):
    config_path = op.join(get_config_dir(), f'{name}.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    config['config_path'] = config_path
    config['experiment_path'] = op.join(base_config['experiment_path'], name)
    get_resource_manager(config)['experiment']
    return


if __name__ == '__main__':
    base_config = get_config('config_path', 'experiment_path')
    # default option: flair space, no mask
    config = fill_config(
        base_config, target='target_flairspace',
        modalities=['t1_flairspace', 'flair_flairspace']
    )
    build_experiment(config, 'flair_space_without_mask')
    # flair space with mask
    config = fill_config(
        base_config, target='target_flairspace',
        modalities=['t1_flairspace', 'flair_flairspace',
                    'brainmask_flairspace'],
    )
    build_experiment(config, 'flair_space_with_mask')
    # t1 space without mask
    config = fill_config(
        base_config, target='target', modalities=['t1', 'flair'],
    )
    build_experiment(config, 't1_space_without_mask')
    # t1 space with mask
    config = fill_config(
        base_config, target='target', modalities=['t1', 'flair', 'brainmask'],
    )
    build_experiment(config, 't1_space_with_mask')
    # t1 space with mask and ANTs nu correction
    config = fill_config(
        base_config, target='target',
        modalities=['t1_antsn3', 'flair_antsn3', 'brainmask'],
    )
    build_experiment(config, 't1_space_mask_ants')
    # t1 space with mask and FreeSurfer nu correction
    config = fill_config(
        base_config, target='target',
        modalities=['t1_fsn3', 'flair_fsn3', 'brainmask'],
    )
    build_experiment(config, 't1_space_mask_fs')
    # t1 space with mask, nu correction, and WM mask
    config = fill_config(
        base_config, target='target',
        modalities=['t1_antsn3', 'flair_antsn3',
                    'T1w_bias_corrected_ants_n4_labeled'],
    )
    config['dataset_masked']['params']['mask_value'] = 3
    build_experiment(config, 't1_space_mask_ants_wm-mask')
