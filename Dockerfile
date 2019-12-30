FROM python:3-alpine
LABEL maintainer="Richard Arends"

ENV MQTT_HOST=localhost
ENV MQTT_USER=root
ENV MQTT_PASSWORD=password

RUN mkdir -p /usr/local/app
WORKDIR /usr/local/app

COPY requirements.txt /usr/local/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY src/* /usr/local/app/

# Expose the Flask port
EXPOSE 8081

CMD [ "/bin/sh", "/usr/local/app/run.sh" ]
