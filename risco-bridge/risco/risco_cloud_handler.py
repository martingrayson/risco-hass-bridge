import requests
from tenacity import wait_exponential, retry

from hass.static import AlarmState
from risco.static import RISCO_BASE_URL, ENDPOINTS, AlarmCommand
from util.logging_mixin import LoggingMixin


# TODO: This credential handling is dumb, maybe use marshmallo with 2 schemas and one auth object.

class RiscoCloudHandler(LoggingMixin):
    """
    Handle all interaction with the Risco Cloud.
    """

    def __init__(self, user_auth, pin_auth):
        """
        Construct a handler using the supplied credentials.
        :param user_auth:
        :param pin_auth:
        """
        self.session = requests.session()
        self.user_auth = user_auth
        self.pin_auth = pin_auth

    def __del__(self):
        """
        Kill session on closing up.
        """
        if self.session:
            self.session.close()

    def login(f):
        """ Decorator to handle logging into Risco """
        def deco(self):
            self.logger.info("Decorating login")
            self._login()
            return f(self)
        return deco

    def _login(self):
        """
        If session has expired, start a new session and login using password and pin.
        """
        if self._is_expired():
            self.session.close()
            self.session = requests.session()

            self._authenticate()
            self._select_site()

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def _authenticate(self):
        """
        First stage in authentication with Risco.
        """
        endpoint = RISCO_BASE_URL + ENDPOINTS['AUTH']
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint, data=self.user_auth.to_json())
        resp.raise_for_status()

        return resp

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def _select_site(self):
        """
        Second stage of authentication with Risco. Selects and activates a site.
        """
        endpoint = RISCO_BASE_URL + ENDPOINTS['SITE_SELECT']
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint, data=self.pin_auth.to_json())
        resp.raise_for_status()

        return resp

    def _is_expired(self) -> bool:
        """
        Checks the Risco endpoint to verify if our session is still active. Any connection errors also return False.
        :return: True if session has expired. False otherwise.
        """
        endpoint = RISCO_BASE_URL + ENDPOINTS['CHECK_EXPIRED']
        self.logger.debug("Hitting: %s" % endpoint)

        try:
            resp = self.session.post(endpoint)
            resp_message = resp.json()
            resp.raise_for_status()
        except Exception as e:
            self.logger.error(e)
            return True

        expired_flag = True
        if resp_message.get('error', 0) == 0 and not resp_message.get('pinExpired', False):
            expired_flag = False

        self.logger.debug("Session active: %s", expired_flag)
        return expired_flag

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    @login
    def _get_overview(self) -> dict:
        """
        Hits the get overview endpoint, returns the json response for downstream mapping into internal states.
        :return: The raw json response in dict form from Risco.
        """
        endpoint = RISCO_BASE_URL + ENDPOINTS['GET_OVERVIEW']
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint)
        resp.raise_for_status()

        return resp.json()

    def get_arm_status(self) -> AlarmState:
        """
        Interprets the Risco get overview function to deterimine if the first partition in the alarm system is
        armed, disarmed or part armed.
        :return: an AlarmState object representing the current state of the system
        """
        sys_overview = self._get_overview()
        part_info = sys_overview.get('overview', {}).get('partInfo', {})

        # Currently unable to cope with partitions being in different states.
        # TODO: Not well guarded, change this.
        state = None
        if int(part_info.get('armedStr')[0]) > 0:
            state = AlarmState.ARMED
        elif int(part_info.get('disarmedStr')[0]) > 0:
            state = AlarmState.DISARMED
        elif int(part_info.get('partarmedStr')[0]) > 0:
            state = AlarmState.PART_ARMED

        self.logger.debug("Alarm state %s", state)

        return state

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    @login
    def set_arm_status(self, arm_status: AlarmCommand) -> dict:
        """
        Sets the alarms arm status, either disarming, arming or part arming the system.
        :param arm_status: an AlarmCommand object representing the desired command to run.
        :return: The raw json response from Risco.
        """
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

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    @login
    def get_state(self) -> dict:
        """
        Gets the state of the control panel.
        :return: The raw json response from Risco.
        """
        endpoint = RISCO_BASE_URL + ENDPOINTS['GET_CP_STATE'] + "?userIsAlive=true"
        self.logger.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint)
        resp.raise_for_status()

        return resp.json()
