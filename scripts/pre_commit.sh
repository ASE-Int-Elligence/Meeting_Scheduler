#!/bin/bash

today=`date '+%Y_%m_%d__%H_%M_%S'`
# # build
pip install -r ../requirements.txt
python ../setup.py install

# style checker, bug finder
cd ../src
filename1="../report/pre_commit/$today-bug.log"
touch $filename1
prospector --strictness veryhigh > $filename1

# testing
cd ../tests

filename2="../report/pre_commit/$today-pytest.log"
touch $filename2
pytest *.py > $filename2



