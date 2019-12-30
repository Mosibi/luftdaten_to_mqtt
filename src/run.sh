#!/bin/bash

EXTRA_ARGS=""

if [ "${DEBUG}" == "1" ]; then
    EXTRA_ARGS="--debug"
fi

/usr/local/bin/python3 \
    -u \
    /usr/local/app/app.py \
    --host "${MQTT_HOST}" \
    --username "${MQTT_USER}" \
    --password "${MQTT_PASSWORD}" \
    "${EXTRA_ARGS}"
