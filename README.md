# Risco Alarm to Home Assistant via MQTT
## Introduction
Monitor and control your Risco alarm using Home Assistant.

This application monitors an MQTT topic and relays commands to the Risco Cloud using their API. This allows you to arm, disarm and part arm your alarm system by publishing messages on the `command` topic.

Another status checker thread polls the Risco API to check the status of your alarm system. Status messages a broadcast on a `state` topic periodically.

*WARNING*: This application was written for my own use, you may use it at your own risk. I can not be held responsible for your use of the information and software contained within this repo. 


## Configuration
The configuration of the plugin is fairly straight forward. You'll need a [Risco Cloud](https://www.riscocloud.com/ELAS/WebUI/) login and an MQTT Broker configured.

The MQTT configuration is self explanatory:
```json
"mqtt": {
      "host": "localhost",
      "port": 1883,
      "username": "Optional username to connect to MQTT",
      "password": "Optional password to connect to MQTT" 
    }
```

Within the Risco Could, it is advisable to create a dedicated service account for this application to use, you can create a new account within the [Web UI](https://www.riscocloud.com/ELAS/WebUI/). The `username`, `password` and `pin` can be added to the plugin config as below:
```json
"risco": {
      "username": "user@test.com",
      "password": "a_secure_password",
      "pin": "1337",
      "site_id": "as_shown_above"
    }
```

To find your `site_id`, login to [Risco Cloud](https://www.riscocloud.com/ELAS/WebUI/) using Chrome. Before entering your PIN, view the source of the page and find the `<div class="site-name"` attribute.
The numerical value in the ID of the div is your site id, i.e. `1337` in the below example.

`<div class="site-name" id="site_1337_div">`

## Integration with Home Assistant
It is possible to integrate this addon with Home Assistant in a few different ways, namely:

### MQTT Alarm Control Panel

It is possible to control and track the status of your alarm system using the native [MQTT Alarm Control Panel](https://www.home-assistant.io/components/alarm_control_panel.mqtt/) component, as pictured below.

```yaml
# Example configuration.yaml entry
alarm_control_panel:
  - platform: mqtt
    state_topic: "home/alarm"
    command_topic: "home/alarm/set"
```

### MQTT Sensor

If you wish to just report the status of your alarm system, you can do this by setting up a [MQTT Sensor](https://www.home-assistant.io/components/sensor.mqtt/) to monitor the state topic. You can also control the arming / disarming of your system by configuring actions on click.

```yaml
# Example configuration.yaml entry
sensor:
  - platform: mqtt
    state_topic: "home/alarm"
```

### MQTT Sensor + Template Sensor

You can enrich the MQTT Sensor by adding an additional templated sensor to customise how you report the state and represent it within the UI.

```yaml
sensor:
    - platform: template
      sensors:
        home_alarm_state:
          friendly_name: "Home Alarm"
          value_template: >-
                {% if is_state('sensor.home_alarm_mqtt', 'disarmed') %}
                  Disarmed
                {% elif is_state('sensor.home_alarm_mqtt', 'armed_away') %}
                  Armed
                {% elif is_state('sensor.home_alarm_mqtt', 'armed_home') %}
                  Part Armed
                {% elif is_state('sensor.home_alarm_mqtt', 'triggered') %}
                  Triggered
                {% else %}
                  Unknown  
                {% endif %}
          icon_template: >-
                {% if is_state('sensor.home_alarm_mqtt', 'disarmed') %}
                  mdi:home-lock-open
                {% elif is_state('sensor.home_alarm_mqtt', 'armed_away') %}
                  mdi:home-lock
                {% elif is_state('sensor.home_alarm_mqtt', 'armed_home') %}
                  mdi:home-lock
                {% elif is_state('sensor.home_alarm_mqtt', 'triggered') %}
                  mdi:bell-ring
                {% else %}
                  mdi:home  
                {% endif %}
```