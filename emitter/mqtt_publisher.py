import paho.mqtt.client as mqtt

# state_topic: "home/alarm"
# command_topic: "home/alarm/set"
#https://www.home-assistant.io/components/alarm_control_panel.mqtt/
client = mqtt.Client()
client.connect("iot.eclipse.org", 1883)
client.publish("paho/temperature", "hello")


#