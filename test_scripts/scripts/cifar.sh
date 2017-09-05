#!/bin/bash
mkdir .cifar10
cd .cifar10
wget -q https://raw.githubusercontent.com/tensorflow/models/master/tutorials/image/cifar10/cifar10.py
wget -q https://raw.githubusercontent.com/tensorflow/models/master/tutorials/image/cifar10/cifar10_input.py
wget -q https://raw.githubusercontent.com/tensorflow/models/master/tutorials/image/cifar10/cifar10_train.py
python cifar10_train.py --max_steps 5000 >> $1
cd ..
rm -r .cifar10