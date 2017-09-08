## Setup
1. Launch an ubuntu-based AWS instance with heavy computational power (e.g. m4.16xlarge), see `aws/aws_config.json` for example.
2. SSH to the instance using `ubuntu` user and your private key from AWS
3. Clone this repo `git clone https://github.com/mibel/mri_segmentation_dl.git`
4. Launch `aws/ami_setup.sh` script (it takes approximately 10-20 minutes)
5. Create a new EBS volume and mount it as /data 
6. SCP the dataset to the /data folder

## Usage
1. To launch a nipype based job you should use docker (miykael/nipype_level4 image has been already pulled).
2. Also it's possible to launch a job using an (executable) python script from `./scripts/run_cmd.py` which automatically wrap command and attach volumes:
```
python scripts/run_cmd.py echo hello world
```
See also `run_cmd.py --help`