#!/usr/bin/env bash

#
# Step 1: set repos name.
#
#REPOS_NAME=jc5x/test-repos-ff3
REPOS_NAME=jc5x/firefly-iii

PLATFORMS=linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v6,linux/386

#
# Step 2: echo some info
#
echo "build-local.sh v1.2: I am building '${VERSION}' for ${REPOS_NAME}."	

if [[ $VERSION == "" ]]; then
	echo 'VERSION seems to be empty, exit.'
	exit 1
fi


# new script start

echo "Current directory is $DIR"

docker version -f '{{.Server.Experimental}}'
docker version

docker run --rm --privileged multiarch/qemu-user-static --reset -p yes i
docker buildx create --name firefly_iii_builder
docker buildx inspect firefly_iii_builder --bootstrap
docker buildx use firefly_iii_builder

# always also push same label as the version (ie develop)
LABEL=$VERSION

# if the version is an alpha version, push to "alpha":
if [[ $VERSION == *"alpha"* ]]; then
	LABEL="alpha"
fi

# if the version is a beta version, push to "beta":
if [[ $VERSION == *"beta"* ]]; then
	LABEL="beta"
fi

if [[ $VERSION != *"beta"* && $VERSION != *"alpha"* && $VERSION != *"develop"* ]]; then
	LABEL="latest"
fi

echo "Version is '$VERSION' so label will be '$REPOS_NAME:$LABEL'."

# build firefly iii
docker buildx build  --build-arg version=$VERSION --platform $PLATFORMS -t $REPOS_NAME:$LABEL --push . -f Dockerfile

if [[ $VERSION != "develop" ]]; then
	echo "Version is '$VERSION' so second label will be '$REPOS_NAME:version-$VERSION'."
	docker buildx build  --build-arg version=$VERSION --platform $PLATFORMS -t $REPOS_NAME:version-$VERSION --push . -f Dockerfile
fi

echo "Done!"
