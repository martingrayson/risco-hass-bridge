import paho.mqtt.publish as publish

from hass.static import AlarmState
from util.logging_mixin import LoggingMixin


class MQTTPublisher(LoggingMixin):

    _STATE_TOPIC = "home/alarm"

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

    # TODO: topic should be param
    def publish_state(self, state: AlarmState):
        if state in AlarmState:
            self.logger.debug(f"Publishing state %s to %s ", state.value, self.host)
            return publish.single(MQTTPublisher._STATE_TOPIC, state.value,
                                  hostname=self.host, port=self.port, auth=self.auth, retain=True)
        raise ValueError("Invalid alarm state: %s" % state)
