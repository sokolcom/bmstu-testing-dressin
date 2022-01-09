import abc
import hashlib

from Repositories.BaseDataBase import BaseRepository, IRepository
from Repositories.ImageRepository import ImageRepository
from config import ip
from typing import Optional, Tuple


class IUserRepository(IRepository):
    @abc.abstractmethod
    def register_user(self, login, name, password, imageid=None) -> Tuple[dict, bool]:
        pass

    @abc.abstractmethod
    def get_user_info(self, login, password) -> Optional[dict]:
        pass

    @abc.abstractmethod
    def user_change_photo(self, login, data) -> Optional[dict]:
        pass

    @abc.abstractmethod
    def user_change_name(self, login, name) -> Optional[str]:
        pass

    # first - response, second - error
    @abc.abstractmethod
    def change_login(self, last_login, new_login) -> Tuple[dict, bool]:
        pass

    @abc.abstractmethod
    def change_password(self, login, password) -> Optional[str]:
        pass

    @abc.abstractmethod
    def get_photo_id_by_login(self, login) -> Optional[int]:
        pass


class UserRepository(BaseRepository, IUserRepository):
    def register_user(self, login, name, password, imageid=None) -> Tuple[dict, bool]:
        try:
            query = "insert into user(user_login, user_name, password, image_id) values ((?), (?), (?), (?))"
            hash = hashlib.md5(password.encode()).hexdigest()
            dataset = tuple([login, name, hash, imageid])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            return self.get_user_info(login, password), False
        except Exception as e:
            if self.enable_log:
                print(f'UserRepository.register_user {e}')
            if e.args[0] == "UNIQUE constraint failed: user.user_login":
                return {"status": "error", "reason": "username already taken"}, True
            else:
                return {"status": "error", "reason": f"internal server error: {e}"}, True

    def get_user_info(self, login, password) -> Optional[dict]:
        try:
            hash = hashlib.md5(password.encode()).hexdigest()
            query = "SELECT user_name, image_id, '" + ip + "/getImage?id='||image_id as image_url, user_login as login from user where user_login = (?) and password = (?);"
            dataset = tuple([login, hash])
            res = dict(self.cursor.execute(query, dataset).fetchone())
            return res
        except Exception as e:
            if self.enable_log:
                print(f'UserRepository.get_user_info {e}')
            return None

    def user_change_photo(self, login, data) -> Optional[dict]:
        try:
            id = self.get_photo_id_by_login(login)
            if id:
                ImageRepository(self.db_name).update_photo(id, data)
            else:
                id = ImageRepository(self.db_name).save_photo(data)
                query = "update user set image_id = (?) where user_login = (?)"
                dataset = tuple([id, login])
                self.cursor.execute(query, dataset)
                self.connect.commit()
            query = "select (?)||image_id as image_url from user where user_login = (?)"
            dataset = tuple([ip + '/getImage?id=', login])
            response = dict(self.cursor.execute(query, dataset).fetchone())
            return response
        except Exception as e:
            if self.enable_log:
                print(f'UserRepository.user_change_photo {e}')
            return None

    def user_change_name(self, login, name) -> Optional[str]:
        try:
            query = "update user set user_name = (?) where user_login = (?);"
            dataset = tuple([name, login])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            return 'OK'
        except Exception as e:
            if self.enable_log:
                print(f'UserRepository.user_change_name {e}')
            return None

    # first - response, second - error
    def change_login(self, last_login, new_login) -> Tuple[dict, bool]:
        try:
            query = "select count(*) from user where user_login = (?)"
            dataset = tuple([new_login])
            num = self.cursor.execute(query, dataset).fetchone()[0]
            if num:
                return {"status": "error", "reason": "username already taken"}, True
            else:
                # Hacker tecnhique, do not repeat at home
                query = "select password, user_name, image_id from user where user_login = (?)"
                dataset = tuple([last_login])
                data = list(self.cursor.execute(query, dataset).fetchone())
                dataset = [new_login]
                for param in data:
                    dataset.append(param)
                dataset = tuple(dataset)

                query = "insert into user(user_login, password, user_name, image_id) values ((?), (?), (?), (?))"
                self.cursor.execute(query, dataset)
                self.connect.commit()

                query = "update wardrobe set wardrobe_owner = (?) where wardrobe_owner = (?)"
                dataset = tuple([new_login, last_login])
                self.cursor.execute(query, dataset)
                self.connect.commit()

                query = "update clothes set owner_login = (?) where owner_login = (?)"
                self.cursor.execute(query, dataset)
                self.connect.commit()

                query = "update wardrobe_user set user_login = (?) where user_login = (?)"
                self.cursor.execute(query, dataset)
                self.connect.commit()

                query = "update invites set login_whom_invites = (?) where login_whom_invites = (?)"
                self.cursor.execute(query, dataset)
                self.connect.commit()

                query = "update invites set login_that_invites = (?) where login_that_invites = (?)"
                self.cursor.execute(query, dataset)
                self.connect.commit()

                query = "delete from user where user_login = (?)"
                dataset = tuple([last_login])
                self.cursor.execute(query, dataset)
                self.connect.commit()

            return {"status": "Ok"}, False
        except Exception as e:
            if self.enable_log:
                print(f'UserRepository.change_login {e}')
            return {"status": "error", "reason": f"internal server error: {e}"}, True


    def change_password(self, login, password) -> Optional[str]:
        try:
            hash = hashlib.md5(password.encode()).hexdigest()
            query = "update user set password = (?) where user_login = (?)"
            dataset = tuple([hash, login])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            return 'OK'
        except Exception as e:
            if self.enable_log:
                print(f'UserRepository.change_password {e}')
            return None

    def get_photo_id_by_login(self, login) -> Optional[int]:
        try:
            query = "select image_id from user where user_login = (?)"
            dataset = tuple([login])
            id = self.cursor.execute(query, dataset).fetchone()[0]
            return id
        except Exception as e:
            if self.enable_log:
                print(f'UserRepository.get_photo_id_by_login {e}')
            return None
