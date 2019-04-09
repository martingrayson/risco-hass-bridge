# import paho.mqtt.subscribe as subscribe
#
#
# def on_message_print(client, userdata, message):
#     print("%s %s" % (message.topic, message.payload))
#
#
# subscribe.callback(on_message_print, "home/alarm/set", hostname="10.0.10.40", port=1883,
#                    auth={"username": "mqtt", "password": "mqtt"})

# inbound states
# Disarm = "DISARM" message on "home/alarm/set" topic
# ARM_HOME
# ARM_AWAY


## MVP - enable or disable alarm.
## get state of alarm (including triggered)

import paho.mqtt.subscribe as subscribe

class MQTTSubscriber(object):

    def __init__(self, host, port=1883, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.auth = {}

        if username:
            self.auth['username'] = self.username
        if password:
            self.auth['password'] = self.password

    def subscribe(self, topic):
        subscribe.callback(self.on_message_print, topic, hostname=self.host, port=self.port, auth=self.auth)

    def on_message_print(self, client, userdata, message):
        print("%s %s" % (message.topic, message.payload))

