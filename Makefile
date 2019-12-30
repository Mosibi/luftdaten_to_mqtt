
all:
	@echo "Use 'make build' to build a container for luftdaten_to_mqtt"

build:
	@podman build --no-cache -t luftdaten_to_mqtt:0.1 .

run:
	@podman run \
		-p 8081:8081 \
		-e MQTT_HOST=localhost \
		-e MQTT_USER=mqttusername \
		-e MQTT_PASSWORD=secretpassword \
		-e DEBUG=1 \
		localhost/luftdaten_to_mqtt:0.1
