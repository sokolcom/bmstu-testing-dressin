from Repositories.UserRepository import IUserRepository
from Repositories.ImageRepository import IImageRepository
import json_routine as js


class UserService:
    repo: IUserRepository
    image_repo: IImageRepository

    def __init__(self, repo: IUserRepository, image_repo: IImageRepository):
        self.repo = repo
        self.image_repo = image_repo

    def login(self, login, password):
        response = self.repo.get_user_info(login, password)
        response_status = 200 if response else 500
        return js.getJSON(response), response_status

    def change_avatar(self, login, file):
        response = self.repo.user_change_photo(login, file)
        response_status = 200 if response else 500
        return js.getJSON(response), response_status

    def change_name(self, login, new_name):
        result = self.repo.user_change_name(login, new_name)
        response_status = 200 if result else 404
        return js.getJSON({"status": result}), response_status

    def change_login(self, login, new_login):
        tuple_response = self.repo.change_login(login, new_login)
        result, error = tuple_response
        response_code = self.__get_resp_code_from_tuple(tuple_response)
        return js.getJSON(result), response_code

    def register(self, login, username, password, file):
        try:
            image = self.image_repo.save_photo(file)
        except Exception:
            image = None
        finally:
            tuple_response = self.repo.register_user(login, username, password, image)
            response, _ = tuple_response
            response_code = self.__get_resp_code_from_tuple(tuple_response)
            return js.getJSON(response), response_code

    def __get_resp_code_from_tuple(self, tuple_response):
        result, error = tuple_response
        if error:
            try:
                if 'internal' in result["reason"]:
                    response_code = 500
                else:
                    response_code = 405
            except Exception:
                response_code = 500
        else:
            response_code = 200
        return response_code