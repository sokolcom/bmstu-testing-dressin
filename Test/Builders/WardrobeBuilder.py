from typing import Optional

from Test.Builders.UserBuilder import UserBuilder


class WardrobeBuilder:
    creator_login: Optional[str] = None
    user_builder: Optional[UserBuilder] = None
    name: str = ""
    description: str = ""
    image = None

    def with_creator_login(self, creator_login: str):
        self.creator_login = creator_login
        return self

    def with_user_builder(self, builder: UserBuilder):
        self.user_builder = builder
        return self

    def with_name(self, name: str):
        self.name = name
        return self

    def with_description(self, description: str):
        self.description = description
        return self

    def with_image(self, image):
        self.image = image
        return self

    def build_create_data(self):
        login = self.creator_login if self.creator_login else self.user_builder.login
        return [login, self.name, self.description, self.image]
