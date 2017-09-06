#! /usr/bin/env python

import cluster_utils as cluster


def parse_arguments():
    # Create argument parser
    parser = cluster.utils.get_standard_parser()
    parser.add_argument('cmd', help='Script to launch',
                        type=str, nargs='+')
    # Parse arguments
    job_kwargs = vars(parser.parse_args())
    cmd = job_kwargs.pop('cmd')
    # drop empty values
    job_kwargs = {key: value for key, value in job_kwargs.items()
                  if value is not None}
    return cmd, job_kwargs


if __name__ == "__main__":
    cmd, job_kwargs = parse_arguments()
    cluster.run_job([' '.join(cmd)], **job_kwargs)
