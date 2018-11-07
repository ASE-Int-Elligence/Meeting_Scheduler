#!/bin/bash

#style checker, bug finder
cd src
today=`date '+%Y_%m_%d__%H_%M_%S'`
filename1="$TRAVIS_BUILD_DIR/report/$today-bug.log"
touch $filename1
prospector --strictness veryhigh > $filename1

#pytest
cd ../tests
filename2="$TRAVIS_BUILD_DIR/report/$today-pytest.log"
touch $filename2
pytest *.py > $filename2