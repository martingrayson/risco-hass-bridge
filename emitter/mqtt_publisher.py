import paho.mqtt.publish as publish

from static import AlarmStates


class MQTTPublisher(object):

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

    def publish_state(self, state):
        if state in AlarmStates:
            return publish.single("home/alarm", state.value, hostname=self.host, port=self.port, auth=self.auth, retain=True)

        raise ValueError("Invalid alarm state: %s" % state)
