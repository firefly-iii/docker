#!/usr/bin/env bash

echo '{"experimental":true}' | sudo tee /etc/docker/daemon.json
mkdir $HOME/.docker
touch $HOME/.docker/config.json
echo '{"experimental":"enabled"}' | sudo tee $HOME/.docker/config.json
sudo service docker restart
docker version -f '{{.Server.Experimental}}'
docker version

TARGET=jc5x/firefly-iii-base-image:latest

ARM32=jc5x/firefly-iii-base-image:latest-arm32v7
ARM64=jc5x/firefly-iii-base-image:latest-arm64
AMD64=jc5x/firefly-iii-base-image:latest-amd64

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

docker manifest create $TARGET $ARM32 $ARM64 $AMD64
docker manifest annotate $TARGET $ARM32 --arch arm   --os linux
docker manifest annotate $TARGET $ARM64 --arch arm64 --os linux
docker manifest annotate $TARGET $AMD64 --arch amd64 --os linux
docker manifest push $TARGET

# download manifest from docker hub for this version, or create one if it doesn't exist.
# append the current target
# push to repository.
