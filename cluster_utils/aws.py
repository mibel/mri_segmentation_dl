import os
from . import utils
from subprocess import check_call


def run_job(cmd, job_name_prefix='', image='miykael/nipype_level4:latest',
            python_path=None, path=None, workdir=None, docker_engine='docker'):
    """Run a job at AWS using SGE provided by CfnCluster

    Parameters
    ----------
    cmd : str
        list of bash command to run
    job_name_prefix: str
        prefix for shell script name
    image : str
        Docker image to use. Can be
            - neuro-dl:latest - Docker for DL
            - neuroimaging:latest - Docker for preprocessing
            - any public Docker image
    python_path: str
        pythonpath to pass to container, i.e. "/home/mibel/dpipe"
    path: str
        path to pass to container, i.e. "/home/mibel/freesurfer"
    workdir: str
        path to start at computing nodes
    docker_engine: str
        'docker' or 'nvidia-docker'

    Examples
    ----------
    """
    user_id, user_name, user_gid = utils.get_system_names_ids(user_id=None)
    if workdir is None:
        workdir = os.getcwd()
    if docker_engine not in ['docker', 'nvidia-docker']:
        raise ValueError('An unknown docker_engine {}'.format(docker_engine))
    # we need two sh scripts
    job_name = utils.get_name(job_name_prefix)
    # the first script is used to launch cmd inside docker image
    cmd = utils.append_paths(cmd, python_path, path)
    cmd_sh = utils.write_sh_script(cmd, '{}_cmd.sh'.format(job_name))
    # the second script is used to launch docker on a node
    image = utils.check_image(image)

    # TODO check the workdir
    job_cmd = [
        '{} run {} /bin/bash -c "{}"'.format(docker_engine, image, cmd_sh),
        '--user {}:{}'.format(user_id, user_gid),
        # '--workdir {}'.format(workdir),
        '--volume /home/{0}:/home/{0}'.format(user_name),
        '--volume {0}:{0}'.format(utils.SHARED_DIR_PATH),
    ]
    job_sh = utils.write_sh_script(job_cmd, '{}.sh'.format(job_name),
                                   delimiter='\\\n\t')
    check_call(['qsub', job_sh])
    return 0
