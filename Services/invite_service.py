import Repositories.InviteRepository as repository
import json_routine as js


class InviteService:
    repo: repository.IInviteRepository

    def __init__(self, repo: repository.IInviteRepository):
        self.repo = repo

    def who_invites_me(self, login: str):
        try:
            data = self.repo.get_invites_by_login(login)
            return js.getJSON(data), 200
        except Exception as e:
            print(f'InviteService.who_invites_me: {e}')
        return None, 500

    def send_invite(self, my_login: str, login_to_invite: str, wardrobe_id: int):
        try:
            tuple_data = self.repo.inviteUser(my_login, login_to_invite, wardrobe_id)
            response_code = self.__get_response_code_from_invite_response(tuple_data)
            response, _ = tuple_data
            return js.getJSON(response), response_code
        except Exception as e:
            print(f'InviteService.send_invite: {e}')
            return None, 500

    def get_wardrobe_users(self, wardrobe_id):
        try:
            response = self.repo.get_wardrobe_editors(wardrobe_id)
            return js.getJSON(response)
        except Exception as e:
            print(f'InviteService.get_wardrobe_users: {e}')
            return None, 500

    def handle_invite(self, invite_id: int, accepted: int):
        try:
            self.repo.handleInvite(invite_id, accepted)
            return 'OK', 200
        except Exception as e:
            print(f'InviteService.handle_invite: {e}')
            return None, 500

    def __get_response_code_from_invite_response(self, tuple_data):
        status, error = tuple_data
        if not error:
            return 200
        try:
            if "internal" in status["reason"]:
                return 500
            if "no such" in status["reason"]:
                return 405
            else:
                return 500
        except Exception:
            return 500
