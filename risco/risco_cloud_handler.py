import logging

import requests

from risco.static import RISCO_BASE_URL, ENDPOINTS


# TODO: Remove stupid error logic and use raise_for_status, catch this and try to login.
# TODO: Close session

# TODO: Add auth types
class RiscoCloudHandler(object):

    # TODO: This credential handling is dumb, maybe use marshmallo with 2 schemas and one auth object.
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
        logging.debug("Hitting: %s" % endpoint)
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
        logging.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint, data=self.pin_auth.to_json())

        return self._set_session_active(resp)

    def get_overview(self):
        endpoint = RISCO_BASE_URL + ENDPOINTS['GET_OVERVIEW']
        logging.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint)

        return resp.json()

    def get_state(self):
        endpoint = RISCO_BASE_URL + ENDPOINTS['GETCPSTATE'] + "?userIsAlive=true"
        logging.debug("Hitting: %s" % endpoint)
        resp = self.session.post(endpoint)

        return resp.json()
