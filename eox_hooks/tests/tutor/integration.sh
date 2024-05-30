#!/bin/bash

# Install the package in the edxapp env
echo "Install package"
pip install -e ../eox-hooks

# Install test requirements from openedx
echo "Install test-requirements"
make test-requirements

# Running the tests using the tutor settings
echo "Run tests"
pytest -s --ds=lms.envs.tutor.test /openedx/eox-hooks/eox_hooks/tests/tutor
