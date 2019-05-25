# Risco Alarm to Home Assistant via MQTT
## Introduction
Monitor and control your Risco alarm using Home Assistant.

This application monitors an MQTT topic and relays commands to the Risco Cloud using their API. This allows you to arm, disarm and part arm your alarm system by publishing messages on the `command` topic.

Another status checker thread polls the Risco API to check the status of your alarm system. Status messages a broadcast on a `state` topic periodically.

*WARNING*: This application was written for my own use, you may use it at your own risk. I can not be held responsible for your use of the information and software contained within this repo. 


## Configuration
TODO

## Home Assistant Setup
TODO
https://www.home-assistant.io/components/alarm_control_panel.mqtt/