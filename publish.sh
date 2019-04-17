#echo "$DOCKER_PASSWORD" | docker login -u ${DOCKER_USERNAME} --password-stdin
#change     --armhf to all
docker run -it --rm --privileged --name "risco-hass-bridge" \
    -v ~/.docker:/root/.docker \
    -v "$(pwd)":/docker \
    hassioaddons/build-env:latest \
    --git \
    --armhf \
    --push \
    --from "homeassistant/{arch}-base" \
    --author "Martin Grayson <martin@mgrayson.co.uk>"