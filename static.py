from enum import Enum


class AlarmStates(Enum):
    DISARMED = "disarmed"
    PART_ARMED = "armed_home"
    ARMED = "armed_away"
    TRIGGERED = "triggered"

