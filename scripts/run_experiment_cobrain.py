#! /usr/bin/env python

import cluster_utils as cluster
from os import path as op


def parse_arguments():
    # Create argument parser
    parser = cluster.utils.get_standard_parser()
    parser.add_argument('exp_dir', help='Path to dir with experiments',
                        type=str)
    # Parse arguments
    job_kwargs = vars(parser.parse_args())
    exp_dir = job_kwargs.pop('exp_dir')
    # drop empty values
    job_kwargs = {key: value for key, value in job_kwargs.items()
                  if value is not None}
    return exp_dir, job_kwargs


if __name__ == "__main__":
    exp_dir, job_kwargs = parse_arguments()
    subdir_template = op.join(exp_dir, 'experiment_')
    i = 0
    while True:
        exp_subdir = '{}{}'.format(subdir_template, i)
        if not op.isdir(exp_subdir):
            break
        cmd = ['cd {}; snakemake'.format(exp_subdir)]
        cluster.run_cobrain_job(cmd, job_name_suffix=i, **job_kwargs)
        i += 1
