import abc

import json_routine as js
from Repositories.BaseDataBase import BaseRepository, IRepository
from config import ip
from typing import Optional

class ILookRepository(IRepository):
    @abc.abstractmethod
    def get_look_by_wardrobe(self, wardrobe_id):
        pass

    @abc.abstractmethod
    def create_look(self, item_ids, look_name, wardrobe_id, image=None) -> Optional[dict]:
        pass

    @abc.abstractmethod
    def get_look_items(self, look_id):
        pass

    @abc.abstractmethod
    def append_items_into_look(self, look_id, item_id):
        pass

    @abc.abstractmethod
    def update_look_items(self, look_id, item_ids):
        pass

    @abc.abstractmethod
    def remove_item_from_look_by_id(self, look_id, item_id):
        pass

    @abc.abstractmethod
    def get_look_by_id(self, look_id):
        pass

    @abc.abstractmethod
    def update_look(self, look_id, new_name, image_id):
        pass

    @abc.abstractmethod
    def remove_look(self, look_id):
        pass

    @abc.abstractmethod
    def get_photo_id_by_look_id(self, look_id):
        pass


class LookRepository(BaseRepository, ILookRepository):
    def get_look_by_wardrobe(self, wardrobe_id):
        try:
            query = "select l.look_id as look_id, look_image_id as image_id, look_name, (?) || look_image_id as image_url from wardrobe_look join look l on wardrobe_look.look_id = l.look_id where wardrobe_id = (?);"
            ip_param = ip + '/getImage?id='
            dataset = tuple([ip_param, wardrobe_id])
            rows = self.cursor.execute(query, dataset)
            response = []
            for row in rows:
                response.append(dict(row))
            return js.getJSON(response)
        except Exception as e:
            if self.enable_log:
                print(f'LookRepository.get_look_by_wardrobe: {e}')
            return None

    def create_look(self, item_ids, look_name, wardrobe_id, image=None) -> Optional[dict]:
        try:
            id = image
            query = "insert into look(look_image_id, look_name) values ((?), (?))"
            dataset = tuple([id, look_name])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            look_id = self.cursor.execute("select distinct last_insert_rowid() from look;").fetchall()[0][0]
            for item_id in item_ids:
                query = "insert into look_clothes(look_id, clothes_id) values ((?), (?))"
                dataset = tuple([look_id, item_id])
                self.cursor.execute(query, dataset)
                self.connect.commit()

            query = 'insert into wardrobe_look(wardrobe_id, look_id) values ((?), (?))'
            dataset = tuple([wardrobe_id, look_id])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            return {"look_id": look_id}
        except Exception as e:
            if self.enable_log:
                print(f'LookRepository.create_look: {e}')
            return None

    def get_look_items(self, look_id):
        try:
            query = "select look_id, look_name from look where look_id = (?);"
            dataset = tuple([look_id])
            try:
                tmp = self.cursor.execute(query, dataset).fetchall()[0]
                result = dict(tmp)
            except Exception as e:
                if self.enable_log:
                    print(f'LookRepository.get_look_items: {e}')
                return None

            query = "select distinct type from clothes join look_clothes lc on clothes.clothes_id = lc.clothes_id where lc.look_id = (?);"
            dataset = tuple([look_id])
            tmp = self.cursor.execute(query, dataset).fetchall()
            categories = []
            for i in tmp:
                categories.append(i[0])
            result["categories"] = categories

            query = "select lc.clothes_id, type as category, clothes_name, image_id, '" + ip + "/getImage?id='||image_id as image_url from clothes join look_clothes lc on clothes.clothes_id = lc.clothes_id where lc.look_id = (?);"
            dataset = tuple([look_id])
            tmp = self.cursor.execute(query, dataset)
            items = []
            for item in tmp:
                items.append(dict(item))

            result["items"] = items
            return js.getJSON([result])
        except Exception as e:
            if self.enable_log:
                print(f'LookRepository.get_look_items: {e}')
            return None

    def append_items_into_look(self, look_id, item_id):
        try:
            query = "insert into look_clothes(look_id, clothes_id) values ((?), (?))"
            dataset = tuple([look_id, item_id])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            return 'Ok'
        except Exception as e:
            if self.enable_log:
                print(f'LookRepository.append_items_into_look: {e}')
            return None

    def update_look_items(self, look_id, item_ids):
        try:
            query = "delete from look_clothes where look_id = (?)"
            dataset = tuple([look_id])
            self.cursor.execute(query, dataset)
            self.connect.commit()

            for item in item_ids:
                query = "insert into look_clothes(look_id, clothes_id) values ((?), (?))"
                dataset = tuple([look_id, item])
                self.cursor.execute(query, dataset)
                self.connect.commit()
            return 'Ok'
        except Exception as e:
            if self.enable_log:
                print(f'LookRepository.update_look_items: {e}')
            return None

    def remove_item_from_look_by_id(self, look_id, item_id):
        try:
            query = "delete from look_clothes where look_id = (?) and clothes_id = (?)"
            dataset = tuple([look_id, item_id])
            self.cursor.execute(query, dataset)
            self.connect.commit()
        except Exception as e:
            if self.enable_log:
                print(f'LookRepository.remove_item_from_look_by_id: {e}')
            return None

    def get_look_by_id(self, look_id):
        try:
            query = "select look_name, look_image_id as image_id, (?)||look_image_id as image_url from look where look_id = (?)"
            dataset = tuple([ip + '/getImage?id=', look_id])
            response = dict(self.cursor.execute(query, dataset).fetchone())
            return [response]
        except Exception as e:
            if self.enable_log:
                print(f'LookRepository.get_look_by_id: {e}')
            return None

    def update_look(self, look_id, new_name, image_id):
        try:
            if new_name:
                query = "update look set look_name = (?) where look_id = (?)"
                dataset = tuple([new_name, look_id])
                self.cursor.execute(query, dataset)
                self.connect.commit()
                return {"status": "OK"}
            if image_id:
                query = "update look set look_image_id = (?) where look_id = (?)"
                dataset = tuple([image_id, look_id])
                self.cursor.execute(query, dataset)
                self.connect.commit()
        except Exception as e:
            if self.enable_log:
                print(f'LookRepository.update_look: {e}')
            return None

    def remove_look(self, look_id):
        try:
            dataset = tuple([look_id])

            query = "delete from look_clothes where look_id = (?)"
            self.cursor.execute(query, dataset)
            self.connect.commit()

            query = "delete from wardrobe_look where look_id = (?)"
            self.cursor.execute(query, dataset)
            self.connect.commit()

            id = self.cursor.execute("select look_image_id from look where look_id = " + look_id).fetchone()[0]

            query = "delete from look where look_id = (?)"
            self.cursor.execute(query, dataset)
            self.connect.commit()

            if id:
                self.cursor.execute("delete from image where image_id = " + str(id))
                self.connect.commit()

            return 'OK'
        except Exception as e:
            if self.enable_log:
                print(f'LookRepository.remove_look: {e}')
            return None

    def get_photo_id_by_look_id(self, look_id):
        try:
            query = "select look_image_id from look where look_id = (?)"
            dataset = tuple([look_id])
            id = self.cursor.execute(query, dataset).fetchone()[0]
            return id
        except Exception as e:
            if self.enable_log:
                print(f'LookRepository.get_photo_id_by_look_id: {e}')
            return None
