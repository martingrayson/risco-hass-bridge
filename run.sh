#!/bin/bash
set -e

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
fi

#/risco-entrypoint.sh --mqtt localhost:1883