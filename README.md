# Luftdaten to MQTT
Publish data recieved from a luftdaten sensor on a MQTT topic. 

A luftdaten sensor (see below) has the abbility to send the data to the luftdaten.info website, and could be configured to sent data to a REST API. 

## luftdaten.info
[Luftdaten.info](hhttps://luftdaten.info/en/home-en/)
 is a project that visualizes air quality data that is recieved from sensors all over the world. If you would like to a build a sensor yourself, they provide you with a shopping list for the hardware, building steps and the firmware to make your sensor working.

## Installation
Copy the file src/app.py and requirements.txt to a location on your host and install the Python dependencies with

```lang=shell
# pip install --no-cache-dir -r requirements.txt
```

## Run as container
To run this project withn a container (that is how i run it), download this project and run `make build` or `docker build --no-cache -t luftdaten_to_mqtt:0.1 .`

The container should be provided with the mqtt hostname, mqtt user and mqtt password

```lang=shell
podman run \
	-p 8081:8081 \
	-e MQTT_HOST=my.host.name \
	-e MQTT_USER=mqttusername \
	-e MQTT_PASSWORD=secretpassword \
	-e DEBUG=1 \
	localhost/luftdaten_to_mqtt:0.1
```



