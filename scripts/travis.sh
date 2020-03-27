#!/usr/bin/env bash

echo "travis.sh: I am building version '${VERSION}' on architecture ${ARCH}."
echo "travis.sh: I am version 1.0 of this script."

#
# Configure Docker.
#
echo "Configuring Docker..."
echo '{"experimental":true}' | sudo tee /etc/docker/daemon.json
mkdir $HOME/.docker
touch $HOME/.docker/config.json
echo '{"experimental":"enabled"}' | sudo tee $HOME/.docker/config.json
sudo service docker restart

#
# easy switch between test and pr repository.
#

#REPOS_NAME=jc5x/ff-test-builds
REPOS_NAME=jc5x/firefly-iii

#
# Login to Docker
#
echo "Logging into Docker..."
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

#
# If ARCH is "arm", do some extra stuff:
#
if [[ $ARCH == "arm" ]]; then
    echo "Because architecture is $ARCH running some extra commands."
    docker run --rm --privileged multiarch/qemu-user-static:register --reset

    # get qemu-arm-static binary
    mkdir tmp
    pushd tmp && \
    curl -L -o qemu-arm-static.tar.gz https://github.com/multiarch/qemu-user-static/releases/download/v2.6.0/qemu-arm-static.tar.gz && \
    tar xzf qemu-arm-static.tar.gz && \
    popd
fi

#
# if the VERSION is "develop", build and push develop, and do nothing else.
# 
if [[ $VERSION == "develop" ]]; then
    BUILDLABEL=$REPOS_NAME:develop-$ARCH
    echo "VERSION is $VERSION. Will build and push $BUILDLABEL."
    docker build -t $BUILDLABEL --build-arg version=${VERSION} -f Dockerfile.$ARCH .
    docker push $BUILDLABEL
else
    echo "'$VERSION' is not 'develop', skip this step."
fi

#
# If the version seems to be an alpha version:
# - build 'alpha-$ARCH'
#
if [[ $VERSION == *"alpha"* ]]; then
    BUILDLABEL=$REPOS_NAME:alpha-$ARCH
    echo "Version is alpha version '$VERSION'. Will build and push '$BUILDLABEL'."
    docker build -t $BUILDLABEL --build-arg version=${VERSION} -f Dockerfile.$ARCH .
    docker push $BUILDLABEL
else
    echo "'$VERSION' is NOT an alpha build. Step will be skipped."
fi

#
# If the version seems to be a beta version:
# - build    'beta-$ARCH'
#
if [[ $VERSION == *"beta"* ]]; then
    BUILDLABEL=$REPOS_NAME:beta-$ARCH
    echo "Version is beta version '$VERSION'. Will build and push '$BUILDLABEL'."
    docker build -t $BUILDLABEL --build-arg version=${VERSION} -f Dockerfile.$ARCH .
    docker push $BUILDLABEL
else
    echo "'$VERSION' is NOT a beta build. Step will be skipped."
fi

#
# If nothing else, build as release:
# - build   'stable-$ARCH'
# - tag as  'latest-$ARCH'
#
if [[ $VERSION != *"beta"* && $VERSION != *"alpha"* ]]; then
    echo "'$VERSION' is not beta or alpha. Build it."

    # first build stable
    BUILDLABEL=$REPOS_NAME:stable-$ARCH
    echo "VERSION is '$VERSION'. Will build and push $BUILDLABEL"
    docker build -t $BUILDLABEL --build-arg version=${VERSION} -f Dockerfile.$ARCH .
    docker push $BUILDLABEL

    # then tag as latest and push:
    docker tag $BUILDLABEL $REPOS_NAME:latest-$ARCH
    docker push $REPOS_NAME:latest-$ARCH
    echo "Also tagged $BUILDLABEL as $REPOS_NAME:latest-$ARCH and pushed"
else
    echo "'$VERSION' is NOT a stable build. Step will be skipped."
fi


# finally, tag a version and push:

VERSIONLABEL=$REPOS_NAME:release-$VERSION-$ARCH
echo "Version is '$VERSION'. Will also push label '$VERSIONLABEL'"
docker tag $BUILDLABEL $VERSIONLABEL
docker push $VERSIONLABEL
