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

#
# Merge alpha
#
if [[ $VERSION == *"alpha"* ]]; then
    TARGET=$REPOS_NAME:alpha
    ARM32=$REPOS_NAME:alpha-arm
    ARM64=$REPOS_NAME:alpha-arm64
    AMD64=$REPOS_NAME:alpha-amd64

    echo "VERSION is '$VERSION'."
    echo "Push alpha-* builds to $TARGET"

    docker manifest create $TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $TARGET
else
    echo "VERSION '$VERSION' is not an alpha version, skip this step."
fi

#
# Merge beta
#
if [[ $VERSION == *"beta"* ]]; then
    TARGET=$REPOS_NAME:beta
    ARM32=$REPOS_NAME:beta-arm
    ARM64=$REPOS_NAME:beta-arm64
    AMD64=$REPOS_NAME:beta-amd64

    echo "VERSION is '$VERSION'."
    echo "Push beta-* builds to $TARGET"

    docker manifest create $TARGET $ARM32 $ARM64 $AMD64
    docker manifest annotate $TARGET $ARM32 --arch arm   --os linux
    docker manifest annotate $TARGET $ARM64 --arch arm64 --os linux
    docker manifest annotate $TARGET $AMD64 --arch amd64 --os linux
    docker manifest push $TARGET
else
    echo "VERSION '$VERSION' is not a beta version, skip this step."
fi

#
# Merge latest (stable)
#
if [[ $VERSION != *"alpha"* && $VERSION != *"beta"* ]]; then
    echo "VERSION is '$VERSION', not alpha and not beta."

    TARGET=$REPOS_NAME:stable
    ARM32=$REPOS_NAME:stable-arm
    ARM64=$REPOS_NAME:stable-arm64
    AMD64=$REPOS_NAME:stable-amd64

    echo "Push latest-* builds to $TARGET"

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

else
    echo "VERSION '$VERSION' is not a stable version, skip this step."
fi

#
# Push the new version tags as well:
#
VERSION_TARGET=$REPOS_NAME:release-$VERSION
VERSION_ARM32=$REPOS_NAME:release-$VERSION-arm
VERSION_ARM64=$REPOS_NAME:release-$VERSION-arm64
VERSION_AMD64=$REPOS_NAME:release-$VERSION-amd64

echo "Version release is '$VERSION_TARGET'."
echo "Will merge ARM   release '$VERSION_ARM32' into '$VERSION_TARGET'."
echo "Will merge ARM64 release '$VERSION_ARM64' into '$VERSION_TARGET'."
echo "Will merge AMD64 release '$VERSION_AMD64' into '$VERSION_TARGET'."

docker manifest create $VERSION_TARGET $VERSION_ARM32 $VERSION_ARM64 $VERSION_AMD64
docker manifest annotate $VERSION_TARGET $VERSION_ARM32 --arch arm   --os linux
docker manifest annotate $VERSION_TARGET $VERSION_ARM64 --arch arm64 --os linux
docker manifest annotate $VERSION_TARGET $VERSION_AMD64 --arch amd64 --os linux
docker manifest push $VERSION_TARGET
