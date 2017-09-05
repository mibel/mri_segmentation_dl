#!/usr/bin/env bash

docker build -f $1.dockerfile -t mgmt.cobrain.stech:5000/$1:latest .
docker push mgmt.cobrain.stech:5000/$1:latest