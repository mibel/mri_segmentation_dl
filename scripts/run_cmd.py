#! /usr/bin/env python

import argparse
import os
import grp
import getpass
import warnings
from subprocess import check_call


GROUP_NAME = 'main_group'
SHARED_DIR_PATH = '/data'


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


def parse_arguments():
    # Create argument parser
    parser = get_standard_parser()
    parser.add_argument('cmd', help='Script to launch',
                        type=str, nargs='+')
    # Parse arguments
    job_kwargs = vars(parser.parse_args())
    cmd = job_kwargs.pop('cmd')
    # drop empty values
    job_kwargs = {key: value for key, value in job_kwargs.items()
                  if value is not None}
    return cmd, job_kwargs


def get_system_names_ids():
    user_id = os.getuid()
    user_name = getpass.getuser()
    try:
        user_gid = grp.getgrnam(GROUP_NAME).gr_gid
    except KeyError:
        warnings.warn('Group {} isn\'t found'.format(GROUP_NAME))
        user_gid = grp.getgrnam(user_name).gr_gid
    return user_id, user_name, user_gid


def run_job(cmd, image='miykael/nipype_level4:latest', python_path=None,
            path=None, docker_engine='docker'):
    user_id, user_name, user_gid = get_system_names_ids()
    job_cmd = [
        docker_engine, 'run',
        '--user {}:{}'.format(user_id, user_gid),
        '--volume /home/{0}:/home/{0}'.format(user_name),
        '--volume {0}:{0}'.format(SHARED_DIR_PATH),
	image, '/bin/bash -c', '"{}"'.format(cmd)
    ]
    print(' '.join(job_cmd))
    check_call(' '.join(job_cmd), shell=True)


if __name__ == "__main__":
    cmd, job_kwargs = parse_arguments()
    run_job(' '.join(cmd), **job_kwargs)
