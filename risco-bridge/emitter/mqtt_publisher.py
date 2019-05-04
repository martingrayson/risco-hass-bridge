import paho.mqtt.publish as publish

from hass.static import AlarmStates
from util.logging_mixin import LoggingMixin


class MQTTPublisher(LoggingMixin):

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

    def publish_state(self, state: AlarmStates):
        if state in AlarmStates:
            self.logger.debug(f"Publishing state %s to %s ", state.value, self.host)
            return publish.single("home/alarm", state.value,
                                  hostname=self.host, port=self.port, auth=self.auth, retain=True)
        raise ValueError("Invalid alarm state: %s" % state)
