import os
from os import path as op
import grp
import sys
import datetime
import getpass
import warnings
import glob
import argparse


IMAGES = ['neuro-dl:latest', 'neuroimaging:latest']
GROUP_NAME = 'main_group'
SHARED_DIR_PATH = '/data'
SGE_SH_DIR = '.sge_sh'
YAML_DIR = '.yaml'


def check_image(image, prefix=''):
    if image not in IMAGES:
        # raise ValueError('Image {} isn\'t available'.format(image))
        warnings.warn('An unknown image {}.'.format(image))
    else:
        image = '{}{}'.format(prefix, image)
    return image


def get_system_names_ids(user_id):
    if user_id is None:
        user_id = os.getuid()
    user_name = getpass.getuser()
    try:
        user_gid = grp.getgrnam(GROUP_NAME).gr_gid
    except KeyError:
        warnings.warn('Group {} isn\'t found'.format(GROUP_NAME))
        user_gid = grp.getgrnam(user_name).gr_gid
    return user_id, user_name, user_gid


def write_sh_script(cmd_list, fname, delimiter='\n'):
    # dir for shell scripts
    pwd = op.dirname(op.realpath(__file__))
    sge_sh_dir = op.join(pwd, SGE_SH_DIR)
    if not op.isdir(sge_sh_dir):
        os.mkdir(sge_sh_dir)
    sh_name = op.join(sge_sh_dir, fname)
    with open(sh_name, 'w') as sh_file:
        sh_file.write('#!/bin/bash\n')
        for i, cmd in enumerate(cmd_list):
            if i == len(cmd_list) - 1:
                delimiter = '\n'
            sh_file.write('{}{}'.format(cmd, delimiter))
    return sh_name


def remove_sh_files(verbose=False):
    sge_dir = get_dir(SGE_SH_DIR)
    for fname in glob.glob(op.join(sge_dir, '*.sh')):
        if verbose:
            print(fname)
        os.remove(fname)


def get_name(job_name_prefix, job_name_suffix=''):
    timestamp = datetime.datetime.now().strftime('%Y.%b.%d-%H.%M').lower()
    user_name = getpass.getuser()
    if job_name_prefix != '':
        job_name_prefix += '-'
    job_name = '{}{}-{}'.format(job_name_prefix, user_name, timestamp)
    job_name = job_name.replace('_', '-')
    job_name = job_name.replace(' ', '-')
    job_name = job_name.replace(':', '-')
    # job_name = job_name.replace('.', '-')
    if job_name_suffix != '':
        job_name = '{}-{}'.format(job_name, job_name_suffix)
    return job_name


def check_fname(fname, with_extension=True):
    if not op.isfile(fname):
        return fname
    i = 0
    fname_no_ext = '.'.join(fname.split('.')[:-1])
    ext = fname.split('.')[-1]
    while True:
        new_fname = '{}-{}.{}'.format(fname_no_ext, i, ext)
        if not op.isfile(new_fname):
            break
        i += 1
    return new_fname


def append_paths(cmd, python_path, path, add_conda_to_path=False):
    if python_path is not None:
        cmd = ['export PYTHONPATH="{}:$PYTHONPATH"'.format(python_path)] + cmd
    if path is not None:
        cmd = ['export PATH="{}:$PATH"'.format(path)] + cmd
    if add_conda_to_path:
        conda_path = os.path.dirname(sys.executable)
        cmd = ['export PATH="{}:$PATH"'.format(conda_path)] + cmd
    return cmd


def get_module_parent_dir():
    path = op.split(op.dirname(op.realpath(__file__)))[0]
    return path


def get_dir(dirname, path=None):
    if path is None:
        path = get_module_parent_dir()
    dirname_full = op.join(path, dirname)
    if not op.isdir(dirname_full):
        os.mkdir(dirname_full)
    return dirname_full


def get_nvidia_drivers_path_map():
    return ['/var/lib/nvidia-docker/volumes/nvidia_driver/375.66',
            '/usr/local/nvidia']


def get_standard_parser():
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("-i", "--image", type=str, help='Docker image to use')
    parser.add_argument("-e", "--docker_engine", type=str,
                        help='docker or nvidia-docker')
    parser.add_argument(
        "-p", "--path", type=str,
        help='path to pass to container, i.e. "/home/mibel/freesurfer"')
    parser.add_argument(
        "-pp", "--python_path", type=str,
        help='pythonpath to pass to container, i.e. "/home/mibel/deep_pipe"')
    parser.add_argument("-j", "--job_name_prefix", type=str,
                        help='prefix of a job name')
    return parser
