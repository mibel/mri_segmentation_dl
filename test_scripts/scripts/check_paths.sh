#!/bin/bash
echo $PWD >> $1
echo $PATH >> $1
which python >> $1
which pip >> $1