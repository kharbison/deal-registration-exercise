#!/bin/bash

# setup python module
cd ../db_loader
pip3 install -r requirements.txt
pip3 install -e .
cd -

# setup backend locally
cd ../backend
npm install
cd -

# setup frontend
cd ../frontend
npm install
cd -
