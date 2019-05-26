import argparse
import threading
import time

from emitter.mqtt_publisher import MQTTPublisher
from emitter.mqtt_subscriber import MQTTSubscriber
from hass.static import AlarmCommand
from risco.auth import UserAuth, PinAuth
from risco.risco_cloud_handler import RiscoCloudHandler
from util.logging_mixin import LoggingMixin


class RiscoHassBridge(LoggingMixin):
    def __init__(self, mqtt_host: str, mqtt_port: int, mqtt_username: str, mqtt_password: str, risco_username: str,
                 risco_password: str, risco_pin: int, risco_site_id: str, poll_interval=60):
        self.risco = RiscoCloudHandler(UserAuth(risco_username, risco_password),
                                       PinAuth(risco_pin, risco_site_id))

        self.mqtt_pub = MQTTPublisher(mqtt_host, mqtt_port, mqtt_username, mqtt_password)
        self.mqtt_sub = MQTTSubscriber(mqtt_host, mqtt_port, mqtt_username, mqtt_password)
        self.poll_interval = poll_interval
        self.logger.debug("Initialised RiscoHassBridge")

    def monitor_state(self):
        """Loop and monitor state of the alarm system"""
        self.logger.debug("Starting polling loop (%i sec).", self.poll_interval)

        while True:
            time.sleep(self.poll_interval)
            self.mqtt_pub.publish_state(self.risco.get_arm_status())

    def monitor_commands(self):
        def on_message(client, userdata, message):
            message_raw = message.payload.decode("utf-8")
            self.logger.debug("Got message %s", message_raw)
            command = AlarmCommand[message_raw].value

            if command:
                self.logger.debug("Calling set_arm_status with %s", command)
                self.risco.set_arm_status(command)

        self.logger.debug("Setting up subscription")
        self.mqtt_sub.subscribe(on_message)

    def run(self):
        """Start up all our monitoring threads, wait for them to finish."""
        self.logger.debug("Starting up threads")
        threads = [threading.Thread(target=self.monitor_state, name="state-checker"),
                   threading.Thread(target=self.monitor_commands, name="command-checker")]

        for thread in threads:
            self.logger.debug("Starting %s thread", thread.name)
            thread.start()

        for thread in threads:
            thread.join()

        self.logger.debug("All threads complete")


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
    parser.add_argument('--poll_interval', type=int, default=60, required=False)
    #parser.add_argument('--log-level', required=False) #TODO: Implement

    args = parser.parse_args()
    bridge = RiscoHassBridge(**vars(args))

    bridge.run()


if __name__ == '__main__':
    main()
