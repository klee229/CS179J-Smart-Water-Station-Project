#!/bin/bash

sudo python3 setup.py install
sudo python3 setup.py build
sudo pip3 install --ignore-installed .
