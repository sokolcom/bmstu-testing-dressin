import abc
import hashlib
import sqlite3

import config


class IRepository:
    @abc.abstractmethod
    def is_key_valid(self, key):
        pass


class BaseRepository(IRepository):
    def __init__(self, db_name: str = config.prod_db, enable_log: bool = True):
        self.db_name = db_name
        self.connect = sqlite3.connect(db_name, check_same_thread=False)
        self.connect.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.connect.commit()
        self.enable_log = enable_log

    def __del__(self):
        self.connect.close()

    def is_key_valid(self, key):
        try:
            hash = hashlib.md5(key.encode()).hexdigest()
            query = "select count(*) from api_keys where api_key = (?);"
            dataset = tuple([hash])
            data = self.cursor.execute(query, dataset).fetchall()[0][0]
            return bool(data)
        except Exception as e:
            if self.enable_log:
                print(f'BaseRepository.is_key_valid: {e}')
            return False
