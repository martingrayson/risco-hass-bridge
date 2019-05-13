from enum import Enum

RISCO_BASE_URL = "https://www.riscocloud.com/ELAS/WebUI/"
ENDPOINTS = {
    "AUTH": "",
    "SITE_SELECT": "SiteLogin",
    "GET_EVENT_HISTORY": "EventHistory/Get",
    "GET_OVERVIEW": "Overview/Get",
    "GET_CP_STATE": "Security/GetCPState",
    "SET_ARM_STATUS": "Security/ArmDisarm",
    "CHECK_EXPIRED": "SystemSettings/IsUserCodeExpired"
}

class AlarmCommand(Enum):
    ARM = "armed"
    DISARM = "disarmed"
    PARTARM = "partially"