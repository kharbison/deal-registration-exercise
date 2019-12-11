#/bin/bash

# build images
./build.sh

# stop any existing application containers
./stop.sh

# start application containers
./start.sh