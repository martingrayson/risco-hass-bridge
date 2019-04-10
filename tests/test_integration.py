import os

from emitter.mqtt_publisher import MQTTPublisher
from risco.auth import UserAuth, PinAuth
from risco.risco_cloud_handler import RiscoCloudHandler

#
# sb = MQTTSubscriber("10.0.10.40", username=os.environ['MQTT_USERNAME'], password=os.environ['MQTT_PASSWORD'])
# sb.subscribe("home/alarm/set")
#



# HACK HACK HACK

rch = RiscoCloudHandler(UserAuth(os.environ.get('RISCO_USERNAME'), os.environ.get('RISCO_PASSWORD')),
                        PinAuth(os.environ.get('RISCO_PIN'), os.environ.get('RISCO_SITE_ID')))



rch.login()
rch.select_site()
mp = MQTTPublisher("10.0.10.40", username=os.environ['MQTT_USERNAME'], password=os.environ['MQTT_PASSWORD'])
mp.publish_state(rch.get_arm_status())

