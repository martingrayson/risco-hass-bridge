import os
import unittest

from emitter.mqtt_publisher import MQTTPublisher
from hass.static import AlarmState


class TestMQTTPublisher(unittest.TestCase):

    def setUp(self):
        pass

    def test_publish_invalid_state(self):
        mp = MQTTPublisher("10.0.0.10", username=os.environ['MQTT_USERNAME'], password=os.environ['MQTT_PASSWORD'])
        with self.assertRaises(ValueError):
            mp.publish_state("INVALID")

    def test_publish_valid_state(self):
        mp = MQTTPublisher("10.0.0.10", username=os.environ['MQTT_USERNAME'], password=os.environ['MQTT_PASSWORD'])
        self.assertIsNone(mp.publish_state(AlarmState.TRIGGERED))
