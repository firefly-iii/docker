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
    LABEL=$REPOS_NAME:develop-$ARCH
    echo "VERSION is $VERSION. Will build and push $LABEL."
    docker build -t $LABEL --build-arg version=${VERSION} -f Dockerfile.$ARCH .
    docker push $LABEL
    exit 0
else
    echo "'$VERSION' is not 'develop', skip this step."
fi

#
# If the version seems to be an alpha version, handle it:
#
if [[ $VERSION == *"alpha"* ]]; then
    LABEL=$REPOS_NAME:alpha-$ARCH
    echo "Version is alpha version '$VERSION'. Will build and push '$LABEL'."
    docker build -t $LABEL --build-arg release=${RELEASE} -f Dockerfile.$ARCH .
    docker push $LABEL
    exit 0
else
    echo "'$VERSION' is NOT an alpha build. Step will be skipped."
fi

#
# If the version seems to be a beta version, handle it:
#
if [[ $VERSION == *"beta"* ]]; then
    LABEL=$REPOS_NAME:beta-$ARCH
    echo "Version is beta version '$VERSION'. Will build and push '$LABEL'."
    docker build -t $LABEL --build-arg release=${RELEASE} -f Dockerfile.$ARCH .
    docker push $LABEL
    exit 0
else
    echo "'$VERSION' is NOT a beta build. Step will be skipped."
fi



echo "end of script for now".
exit 0

# if branch = master AND channel = alpha, build and push 'alpha'
if [[ $RELEASE == "master" && $CHANNEL == "alpha" ]]; then

fi

# if branch is master and channel is alpha, build and push 'alpha' and 'beta'.
if [[ $RELEASE == "master" && $CHANNEL == "beta" ]]; then
    LABEL=$REPOS_NAME:beta-$ARCH
    echo "GitHub branch is $RELEASE and channel is $CHANNEL. Will build and push $LABEL"
    docker build -t $LABEL --build-arg release=${RELEASE} -f Dockerfile.$ARCH .
    docker push $LABEL

    # then tag as alpha and push:
    docker tag $LABEL $REPOS_NAME:alpha-$ARCH
    docker push $REPOS_NAME:alpha-$ARCH
    echo "Also tagged $LABEL as $REPOS_NAME:alpha-$ARCH and pushed"
fi

# if branch is master and channel is stable, push 'alpha' and 'beta' and 'stable'.
if [[ $RELEASE == "master" && $CHANNEL == "stable" ]]; then
    # first build stable
    LABEL=$REPOS_NAME:stable-$ARCH
    echo "GitHub branch is $RELEASE and channel is $CHANNEL. Will build and push $LABEL"
    docker build -t $LABEL --build-arg release=${RELEASE} -f Dockerfile.$ARCH .
    docker push $LABEL

    # then tag as beta and push:
    docker tag $LABEL $REPOS_NAME:beta-$ARCH
    docker push $REPOS_NAME:beta-$ARCH
    echo "Also tagged $LABEL as $REPOS_NAME:beta-$ARCH and pushed"

    # then tag as alpha and push:
    docker tag $LABEL $REPOS_NAME:alpha-$ARCH
    docker push $REPOS_NAME:alpha-$ARCH
    echo "Also tagged $LABEL as $REPOS_NAME:alpha-$ARCH and pushed"

    # then tag as latest and push:
    docker tag $LABEL $REPOS_NAME:latest-$ARCH
    docker push $REPOS_NAME:latest-$ARCH
    echo "Also tagged $LABEL as $REPOS_NAME:latest-$ARCH and pushed"
fi

# push to channel 'version' if master + alpha
if [[ $RELEASE == "master" && $CHANNEL == "alpha" ]]; then
    LABEL=$REPOS_NAME:version-$VERSION-$ARCH
    echo "GitHub release is $RELEASE and channel is $CHANNEL. Will also push alpha as $LABEL"
    docker tag $REPOS_NAME:alpha-$ARCH $LABEL
    docker push $LABEL
fi

# push to channel 'version' if master + beta
if [[ $RELEASE == "master" && $CHANNEL == "beta" ]]; then
    LABEL=$REPOS_NAME:version-$VERSION-$ARCH
    echo "GitHub release is $RELEASE and channel is $CHANNEL. Will also push beta as $LABEL"
    docker tag $REPOS_NAME:beta-$ARCH $LABEL
    docker push $LABEL
fi

# push to channel 'version' if master + stable
if [[ $RELEASE == "master" && $CHANNEL == "stable" ]]; then
    LABEL=$REPOS_NAME:version-$VERSION-$ARCH
    echo "GitHub release is $RELEASE and channel is $CHANNEL. Will also push beta as $LABEL"
    docker tag $REPOS_NAME:stable-$ARCH $LABEL
    docker push $LABEL
fi

echo "Done!"
