import abc
from typing import Tuple, Optional, List

from Repositories.BaseDataBase import BaseRepository, IRepository
from config import ip


class IWardrobeRepository(IRepository):

    @abc.abstractmethod
    def create_wardrobe(self, login, name, description=None, image=None) -> Optional[Tuple[str, int]]:
        pass

    @abc.abstractmethod
    def share_wardrobe(self, wardrobeid, invite_login) -> Optional[str]:
        pass

    @abc.abstractmethod
    def get_all_wardrobes_by_login(self, login) -> List[dict]:
        pass

    @abc.abstractmethod
    def delete_wardrobe(self, wardrobe_id, login) -> Optional[str]:
        pass

    @abc.abstractmethod
    def remove_user_from_wardrobe(self, wardrobe_id, login) -> Tuple[dict, bool]:
        pass

    @abc.abstractmethod
    def get_wardrobe_by_id(self, wardrobe_id) -> Optional[dict]:
        pass

    @abc.abstractmethod
    def update_wardrobe(self, wardrobe_id, new_name, image_id) -> Optional[str]:
        pass

    @abc.abstractmethod
    def get_photo_id_by_wardrobe_id(self, look_id) -> Optional[int]:
        pass


class WardrobeRepository(BaseRepository, IWardrobeRepository):
    def create_wardrobe(self, login, name, description=None, image=None) -> Optional[Tuple[str, int]]:
        try:
            ''' First - creating wardrobe '''
            id = image
            query = "insert into wardrobe(wardrobe_description, wardrobe_name, wardrobe_image_id, wardrobe_owner) values ((?), (?), (?), (?))"
            dataset = tuple([description, name, id, login])
            self.cursor.execute(query, dataset)
            self.connect.commit()

            ''' And then duplicating info into table wardrobe-user (many-to-many) '''
            id = self.cursor.execute("select distinct last_insert_rowid() from wardrobe;").fetchall()[0][0]
            query = "insert into wardrobe_user(wardrobe_id, user_login) values ((?), (?))"
            dataset = tuple([id, login])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            return 'OK', id
        except Exception as e:
            if self.enable_log:
                print(f'WardrobeRepository.create_wardrobe {e}')
            return None

    def share_wardrobe(self, wardrobeid, invite_login) -> Optional[str]:
        try:
            query = "insert into wardrobe_user(wardrobe_id, user_login) values ((?), (?))"
            dataset = tuple([wardrobeid, invite_login])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            return 'OK'
        except Exception as e:
            if self.enable_log:
                print(f'WardrobeRepository.share_wardrobe {e}')
            return None

    def get_all_wardrobes_by_login(self, login) -> List[dict]:
        try:
            query = "select distinct w.wardrobe_id as wardrobe_id, w.wardrobe_image_id as image_id, '" + ip + "/getImage?id='|| w.wardrobe_image_id as wardrobe_image, wardrobe_name, wardrobe_description, wardrobe_owner from wardrobe_user join wardrobe w on wardrobe_user.wardrobe_id = w.wardrobe_id where user_login = (?)"
            dataset = tuple([login])
            res = self.cursor.execute(query, dataset).fetchall()
            response = []
            for w in res:
                response.append(dict(w))
            return response
        except Exception as e:
            if self.enable_log:
                print(f'WardrobeRepository.get_all_wardrobes_by_login {e}')
            return None

    def delete_wardrobe(self, wardrobe_id, login) -> Optional[str]:
        try:
            query = "select (?) = wardrobe_owner from wardrobe where wardrobe_id = (?)"
            dataset = tuple([login, wardrobe_id])
            id = int(self.cursor.execute(query, dataset).fetchone()[0])
            if id:
                dataset = tuple([wardrobe_id])
                query = "delete from invites where wardrobe_id = (?)"
                self.cursor.execute(query, dataset)
                self.connect.commit()

                query = """select l.look_image_id from
                            wardrobe w join wardrobe_look wl on w.wardrobe_id = wl.wardrobe_id
                            join look l on wl.look_id = l.look_id
                            where w.wardrobe_id = """ + str(wardrobe_id)
                tmp = self.cursor.execute(query).fetchall()

                query = "delete from look where look_id in (select look_id from wardrobe_look where wardrobe_id = (?))"
                self.cursor.execute(query, dataset)
                self.connect.commit()

                query = "delete from look_clothes where look_id in (select look_id from wardrobe_look where wardrobe_id = (?))"
                self.cursor.execute(query, dataset)
                self.connect.commit()

                query = "delete from wardrobe_look where wardrobe_id = (?)"
                self.cursor.execute(query, dataset)
                self.connect.commit()

                query = "delete from wardrobe_user where wardrobe_id = (?)"
                self.cursor.execute(query, dataset)
                self.connect.commit()

                id = self.cursor.execute(
                    "select wardrobe_image_id from wardrobe where wardrobe_id = " + wardrobe_id).fetchone()[0]

                query = "delete from wardrobe where wardrobe_id = (?)"
                self.cursor.execute(query, dataset)
                self.connect.commit()

                if id:
                    self.cursor.execute("delete from image where image_id = " + str(id))
                    self.connect.commit()

                for i in tmp:
                    id = i[0]
                    if id:
                        self.cursor.execute("delete from image where image_id = " + str(id))
                        self.connect.commit()

                return 'OK'
            else:
                self.remove_user_from_wardrobe(wardrobe_id, login)
                return 'OK'
        except Exception as e:
            if self.enable_log:
                print(f'WardrobeRepository.delete_wardrobe {e}')
            return None

    def remove_user_from_wardrobe(self, wardrobe_id, login) -> Tuple[dict, bool]:
        try:
            query = "select (?) = wardrobe_owner from wardrobe where wardrobe_id = (?)"
            dataset = tuple([login, wardrobe_id])
            id = int(self.cursor.execute(query, dataset).fetchone()[0])
            if not id:
                query = "delete from wardrobe_user where user_login = (?) and wardrobe_id = (?)"
                dataset = tuple([login, wardrobe_id])
                self.cursor.execute(query, dataset)
                self.connect.commit()
                return {"status": 'OK'}, False
            else:
                return {"status": "error", "reason": "Not owner tried to remove owner"}, True
        except Exception as e:
            if self.enable_log:
                print(f'WardrobeRepository.remove_user_from_wardrobe {e}')
            return {"status": "error", "reason": "Internal server error"}, True

    def get_wardrobe_by_id(self, wardrobe_id) -> Optional[dict]:
        try:
            query = "select wardrobe_name, wardrobe_image_id as image_id, (?)||wardrobe_image_id as image_url from wardrobe where wardrobe_id = (?)"
            dataset = tuple([ip + '/getImage?id=', wardrobe_id])
            response = dict(self.cursor.execute(query, dataset).fetchone())
            return response
        except Exception as e:
            if self.enable_log:
                print(f'WardrobeRepository.get_wardrobe_by_id {e}')
            return None

    def update_wardrobe(self, wardrobe_id, new_name, image_id) -> Optional[str]:
        try:
            if new_name:
                query = "update wardrobe set wardrobe_name = (?) where wardrobe_id = (?)"
                dataset = tuple([new_name, wardrobe_id])
                self.cursor.execute(query, dataset)
                self.connect.commit()
            if image_id:
                query = "update wardrobe set wardrobe_image_id = (?) where wardrobe_id = (?)"
                dataset = tuple([image_id, wardrobe_id])
                self.cursor.execute(query, dataset)
                self.connect.commit()
            return 'OK'
        except Exception as e:
            if self.enable_log:
                print(f'WardrobeRepository.update_wardrobe {e}')
            return None

    def get_photo_id_by_wardrobe_id(self, look_id) -> Optional[int]:
        try:
            query = "select wardrobe_image_id from wardrobe where wardrobe_id = (?)"
            dataset = tuple([look_id])
            id = self.cursor.execute(query, dataset).fetchone()[0]
            return id
        except Exception as e:
            if self.enable_log:
                print(f'WardrobeRepository.get_photo_id_by_wardrobe_id {e}')
            return None
