# FROM ami-e6d5c980 
# the base AMI should be prepared by cfncluster team, see possible options here:
#   https://github.com/awslabs/cfncluster/blob/develop/amis.txt

# install the recent nvidia drivers
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
sudo sh -c 'echo "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/cuda.list'
sudo apt-get update && sudo apt-get install -y --no-install-recommends linux-headers-generic dkms cuda-drivers
# a manual way
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

# add current user to the docker group
sudo groupadd docker
sudo gpasswd -a ${USER} docker
sudo service docker restart

# test docker
# docker run hello-world

# nvidia-docker
wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb

# download docker layers & cache image
script_dir="$( cd "$( dirname "$0" )" && pwd )"
cd $script_dir/../docker && docker build -f neuro-dl.dockerfile -t neuro-dl:latest .

# test nvidia-docker
# nvidia-docker run --rm neuro-dl nvidia-smi

# install miniconda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh 
sudo ./Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda3
sudo chmod -R 777 /miniconda3
rm ./Miniconda3-latest-Linux-x86_64.sh

# add path to conda temporary
export PATH=/miniconda3/bin:$PATH

# install libraries
pip install scikit-learn==0.18.2
pip install pandas==0.20.2
pip install matplotlib==2.0.2
pip install seaborn==0.7.0
pip install nibabel==2.1.0
pip install tqdm==4.14.0
pip install scikit-image==0.13.0
pip install snakemake==3.13.3
pip install tensorflow==1.2.1
pip install jupyter

# setup miniconda for all users permanently
echo "PATH=/miniconda3/bin:\$PATH" | sudo tee -a /etc/profile

# setup users
main_group=main_group
sudo groupadd $main_group
cd ../public_keys
shopt -s nullglob
for file in *_rsa.pub; do
    user=${file//_rsa.pub/}
    echo "Adding user $user"
    # create user
    sudo useradd -m -G $main_group,docker 
    # -m -p $(openssl passwd -1 $user) $user -s /bin/bash
    # delete password
    # sudo passwd -d $user
    # add user's public key
    ssh_dir="/home/$user/.ssh"
    sudo mkdir $ssh_dir
    sudo chmod 700 $ssh_dir
    ssh_auth="$ssh_dir/authorized_keys"
    cat $file | sudo tee -a $ssh_auth
    sudo chmod 600 $ssh_auth
    # fix file owner
    sudo chown $user:$main_group $ssh_dir
    sudo chown $user:$main_group $ssh_auth
    # add user to SGE group
    sudo -u sgeadmin -i qconf -am $user
done
# FINALLY: ami-4610f93f