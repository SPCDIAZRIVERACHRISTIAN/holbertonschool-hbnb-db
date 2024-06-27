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


class DBRepository(Repository):
    """This repository implements CRUD operations"""

    def __init__(self, db_session, engine) -> None:
        """This initializes the session for database access"""
        self.db_session = db_session
        self.engine = engine

    def create_table(self):
        Base.metadata.create_all(self.db_session)

    def get_all(self, model_name: str) -> list:
        """Not implemented"""
        return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Not implemented"""

    def reload(self) -> None:
        """Not implemented"""

    def save(self, obj: Base) -> None: #use this as example to fill the rest of methods
        """Saves object in table"""
        instance = obj
        try:
            self.db_session.add(instance)
            self.db_session()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def update(self, obj: Base) -> Base | None:
        """Not implemented"""

    def delete(self, obj: Base) -> bool:
        """Not implemented"""
        return False
