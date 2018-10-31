#!/bin/bash

#style checker, bug finder
cd src
today=`date '+%Y_%m_%d__%H_%M_%S'`
filename1="/home/el/myfile/$today-bug.log"
touch $filename1
prospector --strictness veryhigh > $filename1

#pytest
cd ../tests
touch $filename2
filename2="/home/el/myfile/$today-pytest.log"
pytest *.py > $filename2