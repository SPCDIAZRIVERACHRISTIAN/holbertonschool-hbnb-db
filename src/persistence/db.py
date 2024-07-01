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
from src.models import db
from src.persistence.repository import Repository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


class DBRepository(Repository):
    """Dummy DB repository"""

    def __init__(self) -> None:
        self.__session = db.session
        self.reload()

    def get_all(self, model_name: str) -> list:
        try:
            return self.__session.query(model_name).all()
        except SQLAlchemyError:
            self.__session.rollback()
            return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        try:
            return self.__session.query(model_name).get(obj_id)
        except SQLAlchemyError:
            self.__session.rollback()
            return None

    def reload(self) -> None:
        db.create_all()
        self.__session = db.session


    def save(self, obj: Base) -> None:
        try:
            self.__session.add(obj)
            self.__session.commit()
            print('user added')
        except SQLAlchemyError:
            print("ERROR")
            self.__session.rollback()

    def update(self, obj: Base) -> None:
        try:
            self.__session.commit()
        except SQLAlchemyError:
            self.__session.rollback()

    def delete(self, obj: Base) -> bool:
        try:
            self.__session.delete(obj)
            self.__session.commit()
            return True
        except SQLAlchemyError:
            self.__session.rollback()
            return False
