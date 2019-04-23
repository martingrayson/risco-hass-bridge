#echo "$DOCKER_PASSWORD" | docker login -u ${DOCKER_USERNAME} --password-stdin
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