#!/bin/bash

set -e

# get absolute path to scripts dir
SCRIPTS_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

# build images
${SCRIPTS_DIR}/build.sh

# stop any existing application containers
${SCRIPTS_DIR}/stop.sh

# start application containers
${SCRIPTS_DIR}/start.sh