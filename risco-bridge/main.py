import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mqtt_host', required=True)
parser.add_argument('--mqtt_port', type=int, default=1883, required=False)
parser.add_argument('--mqtt_username', required=False)
parser.add_argument('--mqtt_password', required=False)

args = parser.parse_args()
print(args)
# Do stuff