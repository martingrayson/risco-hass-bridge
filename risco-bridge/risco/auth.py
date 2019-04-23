class UserAuth:
    def __init__(self, username, password, lang='en-gb'):
        self.username = username
        self.password = password
        self.lang = lang

    def to_json(self):
        return {"username": self.username, "password": self.password, "langId": self.lang}


class PinAuth:
    def __init__(self, pin, site_id, lang='en-gb'):
        self.pin = pin
        self.site_id = site_id
        self.lang = lang

    def to_json(self):
        return {"Pin": self.pin, "SelectedSiteId": self.site_id, "langId": self.lang}
