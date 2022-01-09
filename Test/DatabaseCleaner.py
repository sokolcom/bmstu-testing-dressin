from Repositories.BaseDataBase import BaseRepository


class DatabaseCleaner(BaseRepository):
    def clean(self):
        self.cursor = self.connect.cursor()
        self.cursor.execute("delete from wardrobe_user")
        self.cursor.execute("delete from invites")
        self.cursor.execute("delete from wardrobe_look")
        self.cursor.execute("delete from look_clothes")
        self.cursor.execute("delete from look")
        self.cursor.execute("delete from clothes")
        self.cursor.execute("delete from wardrobe")
        self.cursor.execute("delete from user")
        self.cursor.execute("delete from image")
        self.cursor.execute("delete from api_keys")
        self.connect.commit()
        self.cursor.close()
