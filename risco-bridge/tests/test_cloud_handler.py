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
        response = rch.login()
        self.assertIsNone(response)

    def test_select_site(self):
        rch = RiscoCloudHandler(self.user, self.pin)
        response = rch.login()
        self.assertIsNone(response)

    def test_get_state(self):
        rch = RiscoCloudHandler(self.user, self.pin)
        rch.login()
        resp = rch.get_state()

        # shitty test
        self.assertTrue('IsOffline' in resp)

    def test_get_arm_status(self):
        rch = RiscoCloudHandler(self.user, self.pin)
        rch.login()

        # Suboptimal, only passes if im home :( Really need to stub the api
        self.assertEqual(rch.get_arm_status(), AlarmState.DISARMED)
