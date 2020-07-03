#!/bin/bash

echo "Now in finalize-image.sh for Firefly III"
echo "Script version is 1.0.0 (2020-06-07)"
echo "Running as $(whoami)."

echo "Making directories..."
mkdir -p $FIREFLY_PATH/storage/app/public
mkdir -p $FIREFLY_PATH/storage/build
mkdir -p $FIREFLY_PATH/storage/database
mkdir -p $FIREFLY_PATH/storage/debugbar
mkdir -p $FIREFLY_PATH/storage/export
mkdir -p $FIREFLY_PATH/storage/framework/cache/data
mkdir -p $FIREFLY_PATH/storage/framework/sessions
mkdir -p $FIREFLY_PATH/storage/framework/testing
mkdir -p $FIREFLY_PATH/storage/framework/views/twig
mkdir -p $FIREFLY_PATH/storage/framework/views/v1
mkdir -p $FIREFLY_PATH/storage/framework/views/v2
mkdir -p $FIREFLY_PATH/storage/logs
mkdir -p $FIREFLY_PATH/storage/upload

echo "CHOWN..."

chown -R www-data:www-data $FIREFLY_PATH
chmod -R 775 $FIREFLY_PATH/storage

rm -f $FIREFLY_PATH/storage/logs/laravel.log
