import argparse
import time

from emitter.mqtt_publisher import MQTTPublisher
from risco.auth import UserAuth, PinAuth
from risco.risco_cloud_handler import RiscoCloudHandler
from util.logging_mixin import LoggingMixin


class RiscoHassBridge(LoggingMixin):

    def __init__(self, mqtt_host, mqtt_port, mqtt_username, mqtt_password, risco_username,
                 risco_password, risco_pin, risco_site_id, poll_interval=120):
        self.risco = RiscoCloudHandler(UserAuth(risco_username, risco_password),
                                  PinAuth(risco_pin, risco_site_id))

        self.mqtt_pub = MQTTPublisher(mqtt_host, mqtt_port, mqtt_username, mqtt_password)
        self.poll_interval = poll_interval
        self.logger.debug("Initialised RiscoHassBridge")

    def run(self):
        self.logger.debug("Starting polling loop (%i sec).", self.poll_interval)

        while True:
            time.sleep(self.poll_interval)
            self.mqtt_pub.publish_state(self.risco.get_arm_status())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mqtt_host', required=True)
    parser.add_argument('--mqtt_port', type=int, default=1883, required=False)
    parser.add_argument('--mqtt_username', required=False)
    parser.add_argument('--mqtt_password', required=False)
    parser.add_argument('--risco_username', required=True)
    parser.add_argument('--risco_password', required=True)
    parser.add_argument('--risco_pin', required=True)
    parser.add_argument('--risco_site_id', required=True)
    parser.add_argument('--poll_interval', type=int, default=120, required=False)

    args = parser.parse_args()
    bridge = RiscoHassBridge(**vars(args))

    bridge.run()


if __name__ == '__main__':
    main()
