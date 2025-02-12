#!/bin/bash

set -e

# get absolute path to scripts dir
SCRIPTS_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

# set up network and volume
if ! docker network ls | grep deal_reg_app_net; then
    docker network create deal_reg_app_net
fi

if ! docker volume ls | grep postgres_vol; then
    docker volume create postgres_vol
fi

# build backend image
pushd ${SCRIPTS_DIR}/../backend
docker build -t deal-reg-app-backend .
popd

# build frontend image
pushd ${SCRIPTS_DIR}/../frontend
docker build --build-arg VUE_APP_API_URL -t deal-reg-app-frontend .
popd

# get postgres image
docker pull postgres:12
