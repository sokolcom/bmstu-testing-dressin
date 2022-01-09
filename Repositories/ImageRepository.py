import abc

from Repositories.BaseDataBase import BaseRepository


class IImageRepository:
    @abc.abstractmethod
    def save_photo(self, photo):
        pass

    @abc.abstractmethod
    def update_photo(self, id, data):
        pass

    @abc.abstractmethod
    def get_photo(self, id):
        pass

    @abc.abstractmethod
    def update_user_photo(self, id, data):
        pass


class ImageRepository(BaseRepository, IImageRepository):
    def save_photo(self, photo):
        print("saving photo")
        try:
            query = "insert into image (data) values (?)"
            data_tuple = tuple([photo])
            self.cursor.execute(query, data_tuple)
            self.connect.commit()
            id = self.cursor.execute("select distinct last_insert_rowid() from image;").fetchall()[0][0]
            return id
        except Exception as e:
            if self.enable_log:
                print(f'ImageRepository.save_photo: {e}')
            return None

    def update_photo(self, id, data):
        try:
            query = "update image set data =  (?) where image_id = (?)"
            dataset = tuple([data, id])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            return id
        except Exception as e:
            if self.enable_log:
                print(f'ImageRepository.update_photo: {e}')
            return None

    def get_photo(self, id):
        try:
            data = self.cursor.execute("SELECT data from image where image_id = " + str(id)).fetchall()[0][0]
            return data

        except Exception as e:
            if self.enable_log:
                print(f'ImageRepository.get_photo: {e}')
            return None

    def update_user_photo(self, id, data):
        try:
            query = "update image set data = (?) where image_id = (?)"
            dataset = tuple([data, id])
            self.cursor.execute(query, dataset)
            self.connect.commit()
            return id
        except Exception as e:
            if self.enable_log:
                print(f'ImageRepository.update_user_photo: {e}')
            return None
