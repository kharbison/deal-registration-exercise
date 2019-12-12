#!/bin/bash

# setup python module
cd ../db_loader
pip install -r requirements.txt
pip install -e .
cd -

# setup backend locally
cd ../backend
npm install
cd -

# setup frontend
cd ../frontend
npm install
cd -
