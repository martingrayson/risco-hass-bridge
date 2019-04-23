from enum import Enum

from risco.static import AlarmCommands as RiscoAlarmCommands


class AlarmStates(Enum):
    DISARMED = "disarmed"
    PART_ARMED = "armed_home"
    ARMED = "armed_away"
    TRIGGERED = "triggered"

# this is dumb, we're mapping hass enums to risco ones
# change naming or something
class AlarmCommands(Enum):
    DISARM = RiscoAlarmCommands.DISARM
    ARM_HOME = RiscoAlarmCommands.PARTARM
    ARM_AWAY = RiscoAlarmCommands.ARM