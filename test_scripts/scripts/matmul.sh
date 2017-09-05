#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
py_script=$DIR/matmul.py
python $py_script cpu 1000 10 >> $1
python $py_script gpu 1000 10 >> $1
python $py_script gpu 1000 100 >> $1
python $py_script gpu 1000 10000 >> $1
