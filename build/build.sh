#!/bin/bash
set -ev
if [ -z ${TRAVIS_TAG} ]; then
    echo "Untagged build found."
else
    echo "New git tagged build found."
fi

docker run -it --privileged --rm --name "risco-hass-bridge" \
    -v ~/.docker:/root/.docker \
    -v "$(pwd)":/docker \
    hassioaddons/build-env:latest \
    --git \
    --$ARCH \
    --from "homeassistant/{arch}-base" \
    --author "Martin Grayson <martin@mgrayson.co.uk>" \
    --doc-url "https://github.com/martingrayson/risco-hass-bridge" \
    -d "Risco HASS Bridge"

