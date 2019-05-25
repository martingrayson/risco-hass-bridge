import os
import unittest

from hass.static import AlarmState
from risco.auth import PinAuth, UserAuth
from risco.risco_cloud_handler import RiscoCloudHandler


class TestRiscoCloudHandler(unittest.TestCase):

    def setUp(self):
        self.user = UserAuth(os.environ.get('RISCO_USERNAME'), os.environ.get('RISCO_PASSWORD'))
        self.pin = PinAuth(os.environ.get('RISCO_PIN'), os.environ.get('RISCO_SITE_ID'))

    def test_login(self):
        rch = RiscoCloudHandler(self.user, self.pin)
        response = rch._authenticate()
        self.assertTrue(response.status_code == 200)

    def test_select_site(self):
        rch = RiscoCloudHandler(self.user, self.pin)
        response = rch._select_site()
        self.assertTrue(response.status_code == 200)

    def test_get_state(self):
        rch = RiscoCloudHandler(self.user, self.pin)
        resp = rch._get_state()

        # shitty test
        self.assertTrue('IsOffline' in resp)

    def test_get_arm_status(self):
        rch = RiscoCloudHandler(self.user, self.pin)

        # Suboptimal, only passes if im home :( Really need to stub the api
        self.assertEqual(rch.get_arm_status(), AlarmState.DISARMED)
