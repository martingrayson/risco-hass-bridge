from enum import Enum

from risco.static import AlarmCommand as RiscoAlarmCommands


class AlarmState(Enum):
    """ Enum to model alarm states in Home Assistant """
    DISARMED = "disarmed"
    PART_ARMED = "armed_home"
    ARMED = "armed_away"
    TRIGGERED = "triggered"


# this is dumb, we're mapping hass enums to risco ones
# change naming or something
class AlarmCommand(Enum):
    DISARM = RiscoAlarmCommands.DISARM
    ARM_HOME = RiscoAlarmCommands.PARTARM
    ARM_AWAY = RiscoAlarmCommands.ARM
