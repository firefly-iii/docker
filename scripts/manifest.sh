#!/usr/bin/env bash

#
# Configure Docker:
# 

echo '{"experimental":true}' | sudo tee /etc/docker/daemon.json
mkdir $HOME/.docker
touch $HOME/.docker/config.json
echo '{"experimental":"enabled"}' | sudo tee $HOME/.docker/config.json
sudo service docker restart

#
# Login to Docker
#
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

#
# easy switch between test and pr repository.
#
#REPOS_NAME=jc5x/ff-test-builds
REPOS_NAME=jc5x/firefly-iii

#
# OLD CODE REMOVE ME.
# 
# VERSION_TARGET=$REPOS_NAME:release-$VERSION

# if the VERSION is develop, only push the 'develop' tag
if [[ $VERSION == "develop" ]]; then
    TARGET=$REPOS_NAME:develop
    ARM32=$REPOS_NAME:develop-arm
    ARM64=$REPOS_NAME:develop-arm64
    AMD64=$REPOS_NAME:develop-amd64

    echo "VERSION is '$VERSION'."
    echo "Push develop-* builds to $TARGET"

    docker manifest create $TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $TARGET

    echo "Done managing version '$VERSION'. Will now exit."
    exit 0
fi



echo "Done with manifest for now."

exit 0


# if branch = master AND channel = alpha, push 'alpha'
if [[ $RELEASE == "master" && $CHANNEL == "alpha" ]]; then
    TARGET=$REPOS_NAME:alpha
    ARM32=$REPOS_NAME:alpha-arm
    ARM64=$REPOS_NAME:alpha-arm64
    AMD64=$REPOS_NAME:alpha-amd64

    echo "GitHub branch is $RELEASE."
    echo "Channel is $CHANNEL."
    echo "Push alpha-* builds to $TARGET"

    docker manifest create $TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $TARGET

    echo "Push alpha-* builds to $VERSION_TARGET"

    docker manifest create $VERSION_TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $VERSION_TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $VERSION_TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $VERSION_TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $VERSION_TARGET

fi

# if branch is master and channel is alpha, push 'alpha' and 'beta'.
if [[ $RELEASE == "master" && $CHANNEL == "beta" ]]; then
    TARGET=$REPOS_NAME:alpha
    ARM32=$REPOS_NAME:beta-arm
    ARM64=$REPOS_NAME:beta-arm64
    AMD64=$REPOS_NAME:beta-amd64

    echo "GitHub branch is $RELEASE."
    echo "Channel is $CHANNEL."
    echo "Push beta-* builds to $TARGET"

    docker manifest create $TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $TARGET

    TARGET=$REPOS_NAME:beta
    ARM32=$REPOS_NAME:beta-arm
    ARM64=$REPOS_NAME:beta-arm64
    AMD64=$REPOS_NAME:beta-amd64

    echo "Push beta-* builds to $TARGET"

    docker manifest create $TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $TARGET

    echo "Push beta-* builds to $VERSION_TARGET"

    docker manifest create $VERSION_TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $VERSION_TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $VERSION_TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $VERSION_TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $VERSION_TARGET
fi

# if branch is master and channel is stable, push 'alpha' and 'beta' and 'stable'.
if [[ $RELEASE == "master" && $CHANNEL == "stable" ]]; then
    TARGET=$REPOS_NAME:alpha
    ARM32=$REPOS_NAME:stable-arm
    ARM64=$REPOS_NAME:stable-arm64
    AMD64=$REPOS_NAME:stable-amd64

    echo "GitHub branch is $RELEASE."
    echo "Channel is $CHANNEL."
    echo "Push stable-* builds to $TARGET"

    docker manifest create $TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $TARGET

    TARGET=$REPOS_NAME:beta
    ARM32=$REPOS_NAME:stable-arm
    ARM64=$REPOS_NAME:stable-arm64
    AMD64=$REPOS_NAME:stable-amd64

    echo "Push stable-* builds to $TARGET"

    docker manifest create $TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $TARGET

    TARGET=$REPOS_NAME:stable
    ARM32=$REPOS_NAME:stable-arm
    ARM64=$REPOS_NAME:stable-arm64
    AMD64=$REPOS_NAME:stable-amd64

    echo "Push stable-* builds to $TARGET"

    docker manifest create $TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $TARGET

    TARGET=$REPOS_NAME:latest
    ARM32=$REPOS_NAME:stable-arm
    ARM64=$REPOS_NAME:stable-arm64
    AMD64=$REPOS_NAME:stable-amd64

    echo "Push stable-* builds to $TARGET"

    docker manifest create $TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $TARGET

    echo "Push stable-* builds to $VERSION_TARGET"

    docker manifest create $VERSION_TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $VERSION_TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $VERSION_TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $VERSION_TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $VERSION_TARGET
fi

echo 'Done!'
