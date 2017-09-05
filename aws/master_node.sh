# clone the repo
# git clone https://github.com/neuro-ml/cluster-utils.git 

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
ml_group=ml_group
sudo groupadd $ml_group
cd ../public_keys
shopt -s nullglob
for file in *_rsa.pub; do
    user=${file//_rsa.pub/}
    echo "Adding user $user"
    # create user
    sudo useradd -G $ml_group,sudo -m -p $(openssl passwd -1 $user) $user -s /bin/bash
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
	sudo chown $user:$ml_group $ssh_dir
	sudo chown $user:$ml_group $ssh_auth
	# add user to SGE group
	sudo -u sgeadmin -i qconf -am $user
done

# all you should manually add 'main' to user_groups
# sudo -u sgeadmin -i qconf -mq all.q
