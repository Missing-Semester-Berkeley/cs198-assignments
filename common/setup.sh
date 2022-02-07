#!/usr/bin/env bash

add-apt-repository -y ppa:deadsnakes/ppa
apt-get install -y python3.8

python3.8 -m pip install -r /autograder/source/requirements.txt
