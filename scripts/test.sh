#!/bin/bash

# run python module tests
cd ../db_loader
pytest
cd -

# run backend tests
cd ../backend
npm test
cd -