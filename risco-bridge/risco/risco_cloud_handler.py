import requests
import tenacity
from tenacity import wait_exponential

from hass.static import AlarmStates
from risco.static import RISCO_BASE_URL, ENDPOINTS, AlarmCommands
from util.logging_mixin import LoggingMixin


# TODO: Close session and manage better
# TODO: This credential handling is dumb, maybe use marshmallo with 2 schemas and one auth object.


class RiscoCloudHandler(LoggingMixin):

    def __init__(self, user_auth, pin_auth):
        self.session = requests.session()
        self.user_auth = user_auth
        self.pin_auth = pin_auth

    def __del__(self):
        self.session.close()

    def login(self):
        if self._is_expired():
            self.session.close()
            self.session = requests.session()

            self._authenticate()
            self._select_site()

    @tenacity.retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def _authenticate(self):
        endpoint = RISCO_BASE_URL + ENDPOINTS['AUTH']
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint, data=self.user_auth.to_json())
        resp.raise_for_status()

    @tenacity.retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def _select_site(self):
        endpoint = RISCO_BASE_URL + ENDPOINTS['SITE_SELECT']
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint, data=self.pin_auth.to_json())
        resp.raise_for_status()

    # TODO: Make this a decorator
    def _is_expired(self):
        endpoint = RISCO_BASE_URL + ENDPOINTS['CHECK_EXPIRED']
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint)
        resp_message = resp.json()

        try:
            resp.raise_for_status()
        except Exception as e:
            self.logger.error(e)
            return True

        expired_flag = True
        if resp_message.get('error', 0) == 0 and not resp_message.get('pinExpired', False):
            expired_flag = False

        self.logger.debug("Session active: %s", expired_flag)
        return expired_flag

    @tenacity.retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def _get_overview(self):
        self.login()
        endpoint = RISCO_BASE_URL + ENDPOINTS['GET_OVERVIEW']
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint)
        resp.raise_for_status()

        return resp.json()

    def get_arm_status(self):
        sys_overview = self._get_overview()
        part_info = sys_overview.get('overview', {}).get('partInfo', {})

        # Currently unable to cope with partitions being in different states.
        # TODO: Not well guarded, change this.
        state = None
        if int(part_info.get('armedStr')[0]) > 0:
            state = AlarmStates.ARMED
        elif int(part_info.get('disarmedStr')[0]) > 0:
            state = AlarmStates.DISARMED
        elif int(part_info.get('partarmedStr')[0]) > 0:
            state = AlarmStates.PART_ARMED

        self.logger.debug("Alarm state %s", state)

        return state

    @tenacity.retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def set_arm_status(self, arm_status: AlarmCommands):
        self.login()
        endpoint = RISCO_BASE_URL + ENDPOINTS['SET_ARM_STATUS']
        self.logger.debug("Hitting: %s" % endpoint)

        data = {
            "type": "0:{}".format(arm_status.value),
            "bypassZoneId": -1,
            "armcode": ""
        }
        resp = self.session.post(endpoint, data)
        resp.raise_for_status()

        return resp.json()

    @tenacity.retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_state(self):
        self.login()
        endpoint = RISCO_BASE_URL + ENDPOINTS['GET_CP_STATE'] + "?userIsAlive=true"
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint)
        resp.raise_for_status()

        return resp.json()
