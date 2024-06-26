"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""

from src.models.base import Base
from src.persistence.repository import Repository
import os
import json
import sqlite3


class DBRepository(Repository):
    """Dummy DB repository"""

    def __init__(self) -> None:
        """Not implemented"""
        self.HBNB_ENV = os.getenv('HBNB_ENV', "file")
        self.HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        self.HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        self.HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        self.HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
        self.HBNB_ENV = os.getenv('HBNB_ENV')

        if self.HBNB_ENV == 'db':
            self.db_init()
        else:
            self.file_path = 'data.json'
            self.file_init()

    def db_init(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

    def file_init(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)

    def get_all(self, model_name: str) -> list:
        if self.HBNB_ENV == 'db':
            return self.get_all_db(model_name)
        else:
            return self.get_all_file(model_name)

    def get(self, model_name: str, obj_id: str) -> Base | None:
        if self.HBNB_ENV == 'db':
            return self.get_db(model_name, obj_id)
        else:
            return self.get_file(model_name, obj_id)

    def save(self, obj: Base) -> None:
        if self.HBNB_ENV == 'db':
            self.save_db(obj)
        else:
            self.save_file(obj)

    def update(self, obj: Base) -> Base | None:
        if self.HBNB_ENV == 'db':
            return self.update_db(obj)
        else:
            return self.update_file(obj)

    def delete(self, obj: Base) -> bool:
        if self.HBNB_ENV == 'db':
            return self.delete_db(obj)
        else:
            return self.delete_file(obj)

    # Implement the _db and _file methods for each CRUD operation
    # Example for get_all_db and get_all_file
    def get_all_db(self, model_name: str) -> list:
        # Implement database logic
        pass

    def get_all_file(self, model_name: str) -> list:
        # Implement file logic
        pass
