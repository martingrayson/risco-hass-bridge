import os
import unittest

from emitter.mqtt_publisher import MQTTPublisher


class TestMQTTPublisher(unittest.TestCase):

    def setUp(self):
        pass

    def test_publish_invalid_state(self):
        mp = MQTTPublisher("10.0.10.40", username=os.environ['MQTT_USERNAME'], password=os.environ['MQTT_PASSWORD'])
        with self.assertRaises(ValueError):
            mp.publish_state("DUMMY")

    def test_publish_valid_state(self):
        mp = MQTTPublisher("10.0.10.40", username=os.environ['MQTT_USERNAME'], password=os.environ['MQTT_PASSWORD'])
        self.assertIsNone(mp.publish_state("triggered"))
