#!/usr/bin/env bash

# find all dockerfiles and build them
for dockerfile in *.dockerfile; do
    echo 'Building' $dockerfile
    ./build.sh "${dockerfile%.*}"
done
