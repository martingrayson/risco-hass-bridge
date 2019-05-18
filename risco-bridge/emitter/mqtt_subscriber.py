import paho.mqtt.client as mqtt

from util.logging_mixin import LoggingMixin


class MQTTSubscriber(LoggingMixin):

    _COMMAND_TOPIC = "home/alarm/set"

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

        self.client = mqtt.Client()
        self.client.username_pw_set(username=self.username, password=self.password)

    def subscribe(self, callback):
        """ A blocking function to subscribe to the alarm set MQTT topic.
        :param callback: A callback to execute when a message is received.
        """
        self.logger.debug("Starting up subscription")
        self.client.on_message = callback

        self.logger.debug("Connecting to %s %s", self.host, self.port)
        self.client.connect(host=self.host, port=self.port)
        self.logger.debug("Subscribing to %s", MQTTSubscriber._COMMAND_TOPIC)
        self.client.subscribe(MQTTSubscriber._COMMAND_TOPIC, 0)
        self.client.loop_forever()
