## Setup
1. Install CfnCluster
2. Copy aws/cfncluster_config to ~/.cfncluster/config and add your AWS credentials
3. Launch an instance, clone the repo and launch aws/ami_setup.sh.
The setup will take approximately 20 minutes. When it's finished, you need to save the system as AMI.
4. Copy the id of the saved AMI and use it to fill `custom_ami` field

docker run hello-world
nvidia-docker run --rm neuro-dl nvidia-smi

## General notes on AWS usage
1. There is a shared directory /data which is available for all users. 

2. `cluster_utils` lib provides an interface for jobs launching. 

The lib does the following things
 - add the shared data folder and the user's home into a container;
 - add the required paths to python libs (PYTHONPATH) and to binaries (PATH) to a container;
 - wrap any command to be launched inside docker on cluster
3. An example of running a cmd from python
```
from cluster_utils import run_job
cmd = ['echo "hello, world!"']
run_job(cmd, cpu=8, gpu=1, ram=64)
```
4. Also it's possible to launch a job using an (executable) python script from `./scripts/run_cmd_cobrain.py`:
```
python scripts/run_cmd.py echo hello world
```
See also `run_cmd.py --help`

## How to launch dpipe lib experiments
```
git clone https://github.com/neuro-ml/cluster-utils.git
run_experiment.py ~/experiment/ -pp "/home/mibel/neuro/deep_pipe/"
```
where
- we suppose that 
   * `deep_pipe` lib is installed to `/home/mibel/neuro/deep_pipe/`;
   * a dpipe experiment was generated at `~/experiment`.
- `-pp` flag allows to add additional python libraries inside docker. 