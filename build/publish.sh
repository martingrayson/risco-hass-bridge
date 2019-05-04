#!/bin/bash
set -ev

if [ ! -z ${TRAVIS_TAG} ]; then
    echo "Tagged build found. Pushing to Docker with tag 'latest'."
else
    # DIFF="$(git diff HEAD^ HEAD dropbox-sync)"
    # if [ -z $DIFF ]; then
    #     echo "No changes in Dropbox Sync add-on. Skipping docker push."
    #     exit 0
    # fi
    echo "No tag found. Pushing to Docker with tag 'test'."
fi

git status

sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "/home/$USER/.docker" -R

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

docker run -it --rm --privileged --name "risco-hass-bridge" \
    -v ~/.docker:/root/.docker \
    -v "$(pwd)":/docker \
    hassioaddons/build-env:latest \
    --git \
    --$ARCH \
    --push \
    --from "homeassistant/{arch}-base" \
    --author "Martin Grayson <martin@mgrayson.co.uk>" \
    --tag-latest \
    --doc-url "https://github.com/martingrayson/risco-hass-bridge"