# FROM ami-e6d5c980 
# the starting AMI should be prepared by cfncluster teem, see possible options here:
#   https://github.com/awslabs/cfncluster/blob/develop/amis.txt

# recent nvidia drivers
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
sudo sh -c 'echo "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/cuda.list'
sudo apt-get update && sudo apt-get install -y --no-install-recommends linux-headers-generic dkms cuda-drivers
# manual way
#wget http://us.download.nvidia.com/XFree86/Linux-x86_64/375.66/NVIDIA-Linux-x86_64-375.66.run
#chmod +x NVIDIA-Linux-x86_64-375.66.run
#./NVIDIA-Linux-x86_64-375.66.run -x -a 

# docker
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update && sudo apt-get install -y docker-ce

# add user to docker group
sudo groupadd docker
sudo gpasswd -a ${USER} docker
sudo service docker restart

# test docker
docker run hello-world

# nvidia-docker
wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb

# download docker layers & cache image
git clone https://github.com/neuro-ml/cluster-utils.git 
cd cluster-utils/docker && docker build -f ML-Dockerfile -t neuro-dl:latest .

# test nvidia-docker
nvidia-docker run --rm neuro-dl nvidia-smi

# FINALLY: ami-4610f93f