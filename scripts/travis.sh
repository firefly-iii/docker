#!/usr/bin/env bash

#
# Step 1: set repos name.
#
REPOS_NAME=jc5x/firefly-iii

#
# Step 2: echo some info
#
echo "travis.sh v2.0: I am building '${VERSION}' on architecture ${ARCH} for ${REPOS_NAME}."

#
# Step 3: configure docker
#
echo '{"experimental":true}' | sudo tee /etc/docker/daemon.json
mkdir $HOME/.docker
touch $HOME/.docker/config.json
echo '{"experimental":"enabled"}' | sudo tee $HOME/.docker/config.json
sudo service docker restart

#
# Step 4: login to docker
#
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

#
# Step 5: optional ARM package.
#
if [ $ARCH == "arm" ]; then
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
# Step 6: If version is "develop" build and push develop.
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
# Step 7: If version like "alpha", build and push alpha.
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
# Step 8: If version like "beta", build and push beta.
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
# Step 9: If version not like alpha, beta, develop, build and push stable+latest
#
if [[ $VERSION != *"beta"* && $VERSION != *"alpha"* && $VERSION != *"develop"* ]]; then
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

#
# Step 10: If version not like "develop", build and push "version"
#
if [[ $VERSION != "develop" ]]; then
    VERSIONLABEL=$REPOS_NAME:release-$VERSION-$ARCH
    echo "Version is '$VERSION'. Will also push label '$VERSIONLABEL'"
    docker tag $BUILDLABEL $VERSIONLABEL
    docker push $VERSIONLABEL
else
    echo "'$VERSION' is 'develop', so will not push version."
fi

echo "Done!"
