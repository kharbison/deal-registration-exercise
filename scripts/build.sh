#!/bin/bash

set -e

# get absolute path to scripts dir
SCRIPTS_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

# set up network and volume
docker network create deal_reg_app_net
docker volume create postgres_vol

# build backend image
pushd ${SCRIPTS_DIR}/../backend
docker build -t deal-reg-app-backend .
popd

# build frontend image
pushd ${SCRIPTS_DIR}/../frontend
docker build -t deal-reg-app-frontend .
popd

# get postgres image
docker pull postgres:12
