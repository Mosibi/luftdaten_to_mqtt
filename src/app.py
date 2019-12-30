#!/usr/bin/python
"""
Luftdaten to MQTT

Receives messages from a Luftdaten sensor (https://luftdaten.info) and
sends the data to MQTT

Richard Arends
30 December 2019
"""

import sys
import argparse
import time
from flask import Flask, request, json
from flask_mqtt import Mqtt


def info_msg(message):
    print(
        "{0} INFO: {1}".format(
            time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()), message, flush=True
        )
    )


def error_msg(message):
    print(
        "{0} ERROR: {1}".format(
            time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()), message, flush=True
        )
    )
    sys.exit(99)


def warning_msg(message):
    print(
        "{0} WARNING: {1}".format(
            time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()), message, flush=True
        )
    )


def debug_msg(message):
    if debug == True:
        print(
            "{0} DEBUG: {1}".format(
                time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()), message, flush=True
            )
        )


def publish_message(mqtt, mqtt_path, msg):
    mqtt.publish(mqtt_path, payload=msg, qos=0, retain=False)
    time.sleep(0.1)
    debug_msg(
        "published message {0} on topic {1} at {2}".format(
            msg, mqtt_path, time.asctime(time.localtime(time.time()))
        )
    )


def create_app(debug, mqtt, topic_prefix, mqtt_host, mqtt_user, mqtt_password):
    app = Flask(__name__)
    app.config["MQTT_BROKER_URL"] = mqtt_host
    app.config["MQTT_BROKER_PORT"] = 1883
    app.config["MQTT_USERNAME"] = mqtt_user
    app.config["MQTT_PASSWORD"] = mqtt_password
    app.config[
        "MQTT_KEEPALIVE"
    ] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config["MQTT_TLS_ENABLED"] = False

    mqtt.init_app(app)

    @app.route("/", methods=["POST"])
    def api_root():
        """The root route. Expects a json message luftdaten sensor information"""

        if request.headers["Content-Type"] == "application/json":
            parsed_json = json.loads(json.dumps(request.json))

            debug_msg("parsed_json: {}".format(parsed_json))

            try:
                esp8266id = parsed_json["esp8266id"]

                for entry in parsed_json["sensordatavalues"]:
                    topic = "{}/{}/{}".format(
                        topic_prefix, esp8266id, entry["value_type"].lower()
                    )
                    publish_message(mqtt, topic, entry["value"])
            except KeyError as e:
                error_msg(
                    "Missing information in the data recieved from the luftdaten sensor. {}".format(
                        e
                    )
                )

            return "Message recieved"
        else:
            return "Unsupported Content-Type. Only application/json is supported"

    @app.route("/test", methods=["POST"])
    def api_test():
        """Creates a test message for MQTT"""

        try:
            topic = "{}/{}/{}".format(topic_prefix, "testid", "testing")
            publish_message(mqtt, topic, 123)
        except KeyError as e:
            error_msg(
                "Missing information in the data recieved from the luftdaten sensor. {}".format(
                    e
                )
            )

        return "Message recieved"

    return app


def main():
    parser = argparse.ArgumentParser(
        description="Send data recieved from a luftdaten sensor to MQTT."
    )
    parser.add_argument(
        "--port", default=8081, help="TCP port to listen on", required=False, type=int
    )
    parser.add_argument("--host", help="MQTT host", required=True)
    parser.add_argument("--username", help="MQTT username", required=True)
    parser.add_argument("--password", help="MQTT password", required=True)
    parser.add_argument(
        "--topic_prefix", default="luftdaten", help="MQTT topic prefix", required=False
    )
    parser.add_argument(
        "--debug",
        default=False,
        help="Enable debug information",
        required=False,
        action="store_true",
    )
    args = parser.parse_args()

    global debug
    debug = args.debug

    # Setup MQTT handler
    mqtt = Mqtt()

    # Flask
    app = create_app(
        debug=debug,
        mqtt=mqtt,
        topic_prefix=args.topic_prefix,
        mqtt_host=args.host,
        mqtt_user=args.username,
        mqtt_password=args.password,
    )
    app.run(debug=debug, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    sys.exit(main())
