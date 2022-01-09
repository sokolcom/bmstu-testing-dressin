from typing import Optional, Tuple

from Repositories.UserRepository import IUserRepository

class UserMockRepository(IUserRepository):
    def register_user(self, login, name, password, imageid=None) -> Tuple[dict, bool]:
        pass

    def get_user_info(self, login, password) -> Optional[dict]:
        pass

    def user_change_photo(self, login, data) -> Optional[dict]:
        pass

    def user_change_name(self, login, name) -> Optional[str]:
        pass

    def change_login(self, last_login, new_login) -> Tuple[dict, bool]:
        pass

    def change_password(self, login, password) -> Optional[str]:
        pass

    def get_photo_id_by_login(self, login) -> Optional[int]:
        pass

    def is_key_valid(self, key):
        pass