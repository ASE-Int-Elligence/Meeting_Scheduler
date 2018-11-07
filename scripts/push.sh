#!/bin/sh

setup_git() {
  git config --global user.email "jwang0614@gmail.com "
  git config --global user.name "oliwang "
}

commit_log_files() {
    git pull
#   git checkout -b master
    git add . *.log
    git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
    git remote add origin-logs https://${GH_TOKEN}@github.com/ASE-Int-Elligence/Meeting_Scheduler.git
#   git remote add origin-logs https://${GH_TOKEN}@github.com/ASE-Int-Elligence/Meeting_Scheduler.git > /dev/null 2>&1
    # git push --quiet --set-upstream origin-logs master
    git push
}

setup_git
commit_log_files
upload_files