#/bin/bash

# start postgres container
docker run -d \
    --rm \
    -p 5432:5432 \
    --network deal_reg_app_net \
    -v postgres_vol:/var/lib/data \
    --name postgres \
    postgres:12

# start backend contianer
docker run -d \
    --rm \
    --network deal_reg_app_net \
    -p 3000:3000 \
    --name 'deal-reg-app-backend' \
    deal-reg-app-backend

# start frontend container
docker run -d \
    --rm \
    --network deal_reg_app_net \
    -p 8080:80 \
    --name 'deal-reg-app-frontend' \
    deal-reg-app-frontend