#ARG BUILD_FROM
#FROM $BUILD_FROM
FROM homeassistant/i386-homeassistant-base:latest

ENV LANG C.UTF-8

# Setup base
COPY requirements.txt /
RUN apk add --no-cache python3 python3-dev jq && \
    pip3 install -r requirements.txt

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]