#!/usr/bin/env bash

#
# Step 1: set repos name.
#
REPOS_NAME=jc5x/test-repository
#REPOS_NAME=jc5x/firefly-iii

#
# Step 2: echo some info
#
echo "build-travis.sh v1.0: I am building '${VERSION}' for ${REPOS_NAME}."

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# new script start

echo "Current directory is $DIR"

docker version -f '{{.Server.Experimental}}'
docker version

docker run --rm --privileged multiarch/qemu-user-static --reset -p yes i
docker buildx create --name firefly_iii_builder
docker buildx inspect firefly_iii_builder --bootstrap
docker buildx use firefly_iii_builder

PUSHVERSION=$VERSION

#
# Step 10: If version not like "develop", build and push "version"
#
if [[ $VERSION != "develop" ]]; then
    PUSHVERSION=latest
fi

echo "Push version is $PUSHVERSION, version is $VERSION"

# build firefly iii (TODO)
#docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v6 --build-arg version=$VERSION -t $REPOS_NAME:$PUSHVERSION --push . -f Dockerfile --buildarg 
docker buildx build  --build-arg version=$VERSION --platform linux/amd64,linux/arm64,linux/arm/v7 -t $REPOS_NAME:$PUSHVERSION --push . -f Dockerfile

echo "Done!"
