#!/bin/bash

set -e

# get absolute path to scripts dir
SCRIPTS_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

# setup python module
pushd ${SCRIPTS_DIR}/../db_loader
pip3 install -r requirements.txt
pip3 install -e .
popd

# setup backend locally
pushd ${SCRIPTS_DIR}/../backend
npm install
popd

# setup frontend
pushd ${SCRIPTS_DIR}/../frontend
npm install
popd
