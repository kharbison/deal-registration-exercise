#!/bin/bash

set -e

# stop app containers
docker stop deal-reg-app-frontend
docker stop deal-reg-app-backend
docker stop postgres
