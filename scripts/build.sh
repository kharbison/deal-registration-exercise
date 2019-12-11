#/bin/bash

# set up network and volume
docker network create deal_reg_app_net
docker volume create postgres_vol

# build backend image
cd ../backend
docker build -t deal-reg-app-backend .
cd ../

# build frontend image
cd frontend
docker build -t deal-reg-app-frontend .
cd ../

# get postgres image
docker pull postgres:12
