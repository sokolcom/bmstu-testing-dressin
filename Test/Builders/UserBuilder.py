class UserBuilder:
    login = ""
    name = ""
    imageid = None
    password = ""

    def with_name(self, name):
        self.name = name
        return self

    def with_login(self, login):
        self.login = login
        return self

    def with_password(self, password):
        self.password = password
        return self

    def with_imageid(self, imageid):
        self.imageid = imageid
        return self

    def build_login_data(self):
        return [self.login, self.password]

    def build_register_data(self):
        return [self.login, self.name, self.password, self.imageid]
