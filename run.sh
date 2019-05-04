#!/bin/bash
set -e

APP_ENTRYPOINT=risco-bridge/main.py
CONFIG_PATH=/data/options.json
MQTT_CONFIG=

# Use Hass.io mqtt services
if MQTT_CONFIG="$(curl -s -f -H "X-Hassio-Key: ${HASSIO_TOKEN}" http://hassio/services/mqtt)"; then
    HOST="$(echo "${MQTT_CONFIG}" | jq --raw-output '.data.host')"
    PORT="$(echo "${MQTT_CONFIG}" | jq --raw-output '.data.port')"
    USER="$(echo "${MQTT_CONFIG}" | jq --raw-output '.data.username')"
    PASSWORD="$(echo "${MQTT_CONFIG}" | jq --raw-output '.data.password')"

    echo "[INFO] Setup Hass.io mqtt service to ${HOST}"
else
    echo "[ERROR] No Hass.io mqtt service found!"
    exit 1
fi

RISCO_USER=$(jq --raw-output ".risco.username" $CONFIG_PATH)
RISCO_PASSWORD=$(jq --raw-output ".risco.password" $CONFIG_PATH)
RISCO_PIN=$(jq --raw-output ".risco.pin" $CONFIG_PATH)
RISCO_SITE=$(jq --raw-output ".risco.site_id" $CONFIG_PATH)

python3 ${APP_ENTRYPOINT} --mqtt_host ${HOST} --mqtt_port ${PORT} --mqtt_username ${USER} --mqtt_password ${PASSWORD} --risco_username ${RISCO_USER} --risco_password ${RISCO_PASSWORD}  --risco_pin ${RISCO_PIN}  --risco_site_id ${RISCO_SITE}