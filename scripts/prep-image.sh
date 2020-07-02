#!/bin/bash

# also room for more commands in the future.

echo "Now in prep-image.sh for Firefly III"
echo "Script version is 1.0.1 (2020-07-02)"
echo "Running as $(whoami)."

echo "Apache version"
apache2 -v

echo "Making directories..."
mkdir -p $FIREFLY_PATH
