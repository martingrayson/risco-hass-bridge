#echo "$DOCKER_PASSWORD" | docker login -u ${DOCKER_USERNAME} --password-stdin
#change     --armhf to all and add documentation url
docker run -it --rm --privileged --name "risco-hass-bridge" \
    -v ~/.docker:/root/.docker \
    -v "$(pwd)":/docker \
    hassioaddons/build-env:latest \
    --git \
    --armhf \
    --from "homeassistant/{arch}-base" \
    --author "Martin Grayson <martin@mgrayson.co.uk>" \
    --tag-latest \
    --doc-url "https://github.com/martingrayson/risco-hass-bridge"