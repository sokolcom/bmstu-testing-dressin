import abc
from typing import Tuple

from Repositories.BaseDataBase import BaseRepository, IRepository
from config import ip


class IInviteRepository(IRepository):
    @abc.abstractmethod
    def get_wardrobe_editors(self, wardrobe_id):
        pass

    @abc.abstractmethod
    def get_invites_by_login(self, login):
        pass

    @abc.abstractmethod
    def inviteUser(self, my_login, login_whom_to_inivte, wardrobe_id) -> Tuple[dict, bool]:
        pass

    @abc.abstractmethod
    def handleInvite(self, invite_id, accepted):
        pass


class InviteRepository(BaseRepository, IInviteRepository):
    """
    [
        {
            image_url: string?,
            login: string,
            user_name: string,
        }
    ]
    """

    def get_wardrobe_editors(self, wardrobe_id):
        try:
            query = """select (?)||u.image_id as image_url, u.user_login as login, u.user_name as user_name
                        from wardrobe_user join user u on wardrobe_user.user_login = u.user_login
                        where wardrobe_id = (?)"""
            ip_param = ip + '/getImage?id='
            dataset = tuple([ip_param, wardrobe_id])
            res = self.cursor.execute(query, dataset)
            response = []
            for row in res:
                response.append(dict(row))
            return response
        except Exception as e:
            if self.enable_log:
                print(f'InviteRepository.get_wardrobe_editors: {e}')
            return None

    """
    [
        {
            invite_id: int,
            login_that_invites: string,
            wardrobe_name: string,
            image_url: string?
        }
    ]
    """

    def get_invites_by_login(self, login):
        try:
            query = "select invite_id, login_that_invites, w.wardrobe_name as wardrobe_name, '" + \
                    ip + "/getImage?id='||w.wardrobe_image_id as image_url from invites join wardrobe w " \
                         "on invites.wardrobe_id = w.wardrobe_id where login_whom_invites = (?)"
            dataset = tuple([login])
            res = self.cursor.execute(query, dataset)
            response = []
            for row in res:
                response.append(dict(row))
            return response
        except Exception as e:
            if self.enable_log:
                print(f'InviteRepository.get_invites_by_login: {e}')
            return None

    """
        {status: "OK/ERROR", reason: string?}, error: bool
    """

    def inviteUser(self, my_login, login_whom_to_inivte, wardrobe_id) -> Tuple[dict, bool]:
        try:
            query = "select * from wardrobe_user where wardrobe_id = (?) and user_login = (?)"
            dataset = tuple([wardrobe_id, login_whom_to_inivte])
            a = self.cursor.execute(query, dataset).fetchone()
            if a == None:
                query = "insert into invites(login_that_invites, login_whom_invites, wardrobe_id) values ((?), (?), (?));"
                dataset = tuple([my_login, login_whom_to_inivte, wardrobe_id])
                self.cursor.execute(query, dataset)
                self.connect.commit()
                return {"status": "OK"}, False
            else:
                return {"status": "error", "reason": "already in wardrobe"}, True
        except Exception as e:
            try:
                if e.args[0] == "FOREIGN KEY constraint failed":
                    return {"status": "error", "reason": "no such user or wardrobe"}, True
                else:
                    return {"status": "error", "reason": "internal server error"}, True
            except Exception as e:
                if self.enable_log:
                    print(f'InviteRepository.inviteUser: {e}')
                return {"status": "error", "reason": "internal server error"}, True

    def handleInvite(self, invite_id, accepted):
        try:
            query = "select distinct wardrobe_id, login_whom_invites from invites where invite_id = (?);"
            dataset = tuple([invite_id])
            tmp = dict(self.cursor.execute(query, dataset).fetchone())
            wardrobe_id = int(tmp["wardrobe_id"])
            login = tmp["login_whom_invites"]
            if accepted:
                query = "insert into wardrobe_user(wardrobe_id, user_login) values ((?), (?))"
                dataset = tuple([wardrobe_id, login])
                self.cursor.execute(query, dataset)
                self.connect.commit()
            query = "delete from invites where wardrobe_id = (?) and login_whom_invites = (?)"
            dataset = tuple([wardrobe_id, login])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            return "OK"
        except Exception as e:
            if self.enable_log:
                print(f'InviteRepository.handleInvite: {e}')
            return None
