#!/bin/bash

set -e

# stop app containers
if docker ps | grep deal-reg-app-frontend; then
    docker stop deal-reg-app-frontend
fi

if docker ps | grep deal-reg-app-backend; then
    docker stop deal-reg-app-backend
fi

if docker ps | grep postgres; then
    docker stop postgres
fi
