import requests

from hass.static import AlarmStates
from risco.static import RISCO_BASE_URL, ENDPOINTS, AlarmCommands
from util.logging_mixin import LoggingMixin


# TODO: Remove stupid error logic and use raise_for_status, catch this and try to login.
# TODO: Close session and manage better
# TODO: This credential handling is dumb, maybe use marshmallo with 2 schemas and one auth object.

class RiscoCloudHandler(LoggingMixin):

    def __init__(self, user_auth, pin_auth):
        self.session = requests.session()
        self.session_active = False
        self.user_auth = user_auth
        self.pin_auth = pin_auth

    def __del__(self):
        self.session.close()
        self.session_active = False

    def login(self):
        endpoint = RISCO_BASE_URL + ENDPOINTS['AUTH']
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint, data=self.user_auth.to_json())

        return self._set_session_active(resp)

    def _set_session_active(self, resp):
        if resp:
            self.session_active = (200 <= resp.status_code < 400)
        else:
            self.session_active = False

        return self.session_active

    def select_site(self):
        endpoint = RISCO_BASE_URL + ENDPOINTS['SITE_SELECT']
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint, data=self.pin_auth.to_json())

        return self._set_session_active(resp)

    def _get_overview(self):
        endpoint = RISCO_BASE_URL + ENDPOINTS['GET_OVERVIEW']
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint)

        return resp.json()

    def get_arm_status(self):
        sys_overview = self._get_overview()
        part_info = sys_overview.get('overview', {}).get('partInfo', {})

        # Currently unable to cope with partitions being in different states.
        # Not well guarded, change this.
        state = None
        if int(part_info.get('armedStr')[0]) > 0:
            state = AlarmStates.ARMED
        elif int(part_info.get('disarmedStr')[0]) > 0:
            state = AlarmStates.DISARMED
        elif int(part_info.get('partarmedStr')[0]) > 0:
            state = AlarmStates.PART_ARMED

        return state

    def set_arm_status(self, arm_status: AlarmCommands):
        endpoint = RISCO_BASE_URL + ENDPOINTS['SETARMSTATUS']
        self.logger.debug("Hitting: %s" % endpoint)

        data = {
            "type": "0:{}".format(arm_status.value),
            "bypassZoneId": -1,
            "armcode": ""
        }
        resp = self.session.post(endpoint, data)
        return resp.json()

    def get_state(self):
        endpoint = RISCO_BASE_URL + ENDPOINTS['GETCPSTATE'] + "?userIsAlive=true"
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint)

        return resp.json()
