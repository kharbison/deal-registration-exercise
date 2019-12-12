#!/bin/bash

set -e

# get absolute path to scripts dir
SCRIPTS_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

# run python module tests
pushd ${SCRIPTS_DIR}/../db_loader
pytest
popd

# run backend tests
pushd ${SCRIPTS_DIR}/../backend
npm test
popd