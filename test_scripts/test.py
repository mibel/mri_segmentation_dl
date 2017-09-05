#! /usr/bin/env python

import cluster_utils as cluster
import argparse
from os import path as op
from os import remove

CLUSTER_TYPE_MAP = {'aws': cluster.run_aws_job}


def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument('cluster_type', help='Type of cluster to test',
                        type=str, choices=list(CLUSTER_TYPE_MAP.keys()))
    parser.add_argument('script', nargs='?', default='check_paths.sh',
                        help='Name of script', type=str)
    parser.add_argument('-l', "--log_file", default='test_results.txt',
                        help='Name of log_file', type=str)
    parser.add_argument("-e", "--engine", type=str, help='Kubernetes or SGE',
                        default='kubernetes')
    # Parse arguments
    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    args = parse_arguments()
    pwd = op.dirname(op.realpath(__file__))
    log_file = op.join(pwd, args['log_file'])
    if op.isfile(log_file):
        remove(log_file)
    script_full_path = op.join(pwd, 'scripts', args['script'])
    cmd = ['{} {}'.format(script_full_path, log_file)]
    run_job = CLUSTER_TYPE_MAP[args['cluster_type']]
    run_job(cmd, job_name_prefix='test', engine=args['engine'])
