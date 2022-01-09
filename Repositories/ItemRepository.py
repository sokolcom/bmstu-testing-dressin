import abc

from Repositories.BaseDataBase import BaseRepository, IRepository
from config import ip
from typing import Optional


class IItemRepository(IRepository):
    @abc.abstractmethod
    def get_item_by_id(self, item_id) -> Optional[dict]:
        pass

    @abc.abstractmethod
    def add_item(self, owner, name, type, image_id=None) -> Optional[dict]:
        pass

    @abc.abstractmethod
    def update_item(self, item_id, new_name, id) -> Optional[dict]:
        pass

    @abc.abstractmethod
    def remove_item(self, item_id) -> Optional[str]:
        pass

    @abc.abstractmethod
    def get_all_items_by_user(self, login) -> Optional[dict]:
        pass

    @abc.abstractmethod
    def get_photo_id_by_item_id(self, item_id) -> Optional[int]:
        pass


class ItemRepository(BaseRepository, IItemRepository):
    def get_item_by_id(self, item_id) -> Optional[dict]:
        try:
            query = "select *, (?)||image_id as image_url from clothes where clothes_id = (?)"
            ip_param = ip + '/getImage?id='
            dataset = tuple([ip_param, item_id])
            response = self.cursor.execute(query, dataset).fetchone()
            return dict(response)
        except Exception as e:
            if self.enable_log:
                print(f'ItemRepository.get_item_by_id: {e}')
            return None

    def add_item(self, owner, name, type, image_id=None) -> Optional[dict]:
        try:
            query = "insert into clothes(clothes_name, type, image_id, owner_login) values ((?), (?), (?), (?))"
            dataset = tuple([name, type, image_id, owner])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            item_id = self.cursor.execute("select distinct last_insert_rowid() from clothes;").fetchall()[0][0]
            response = {"item_id": item_id}
            return response
        except Exception as e:
            if self.enable_log:
                print(f'ItemRepository.add_item: {e}')
            return None

    def update_item(self, item_id, new_name, id) -> Optional[dict]:
        try:
            if new_name:
                query = "update clothes set clothes_name = (?) where clothes_id = (?)"
                dataset = tuple([new_name, item_id])
                self.cursor.execute(query, dataset)
                self.connect.commit()
            if id:
                query = "update clothes set image_id = (?) where clothes_id = (?)"
                dataset = tuple([id, item_id])
                self.cursor.execute(query, dataset)
                self.connect.commit()
                return "OK"
        except Exception as e:
            if self.enable_log:
                print(f'ItemRepository.update_item: {e}')
            return {"status": "Error", "description": e}

    def remove_item(self, item_id) -> Optional[str]:
        try:
            dataset = tuple([item_id])

            query = "delete from look_clothes where clothes_id = (?)"
            self.cursor.execute(query, dataset)
            self.connect.commit()

            query = "delete from clothes where clothes_id = (?)"
            self.cursor.execute(query, dataset)
            self.connect.commit()
            try:
                id = self.cursor.execute("select image_id from clothes where clothes_id = " + item_id).fetchone()[0]
                if id:
                    self.cursor.execute("delete from image where image_id = " + str(id))
                    self.connect.commit()
            except Exception:
                pass
            return 'OK'
        except Exception as e:
            if self.enable_log:
                print(f'ItemRepository.remove_item: {e}')
            return None

    def get_all_items_by_user(self, login) -> Optional[dict]:
        try:
            response = dict()
            query = "select distinct type from clothes where owner_login = (?)"
            dataset = tuple([login])
            tmp = self.cursor.execute(query, dataset).fetchall()
            categories = []
            for i in tmp:
                categories.append(i[0])
            response["categories"] = sorted(categories)
            query = "select clothes_name, type as category, image_id, clothes_id, '" + ip + "/getImage?id='||image_id as image_url from clothes where owner_login = (?)"
            dataset = tuple([login])
            items = self.cursor.execute(query, dataset)
            response["clothes"] = []
            for item in items:
                response["clothes"].append(dict(item))
            return response
        except Exception as e:
            if self.enable_log:
                print(f'ItemRepository.get_all_items_by_user: {e}')
            return None

    def get_photo_id_by_item_id(self, item_id) -> Optional[int]:
        try:
            query = "select image_id from clothes where clothes_id = (?)"
            dataset = tuple([item_id])
            photo_id = self.cursor.execute(query, dataset).fetchone()[0]
            return photo_id
        except Exception as e:
            if self.enable_log:
                print(f'ItemRepository.get_photo_id_by_item_id: {e}')
            return None
