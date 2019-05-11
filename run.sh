#!/bin/bash
set -e

APP_ENTRYPOINT=risco-bridge/main.py
CONFIG_PATH=/data/options.json

HOST=$(jq --raw-output ".mqtt.host" $CONFIG_PATH)
PORT=$(jq --raw-output ".mqtt.port" $CONFIG_PATH)
USER=$(jq --raw-output ".mqtt.username" $CONFIG_PATH)
PASSWORD=$(jq --raw-output ".mqtt.password" $CONFIG_PATH)

RISCO_USER=$(jq --raw-output ".risco.username" $CONFIG_PATH)
RISCO_PASSWORD=$(jq --raw-output ".risco.password" $CONFIG_PATH)
RISCO_PIN=$(jq --raw-output ".risco.pin" $CONFIG_PATH)
RISCO_SITE=$(jq --raw-output ".risco.site_id" $CONFIG_PATH)

POLL_INTERVAL=$(jq --raw-output ".poll_interval" $CONFIG_PATH)

python3 ${APP_ENTRYPOINT} --poll_interval ${POLL_INTERVAL} --mqtt_host ${HOST} --mqtt_port ${PORT} \
--mqtt_username ${USER} --mqtt_password ${PASSWORD} --risco_username ${RISCO_USER} --risco_password ${RISCO_PASSWORD} \
--risco_pin ${RISCO_PIN}  --risco_site_id ${RISCO_SITE}