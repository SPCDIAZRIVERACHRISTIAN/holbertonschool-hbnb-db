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
from sqlalchemy.exc import SQLAlchemyError
from src.models.base import Base
from src.persistence.repository import Repository
from . import db


class DBRepository(Repository):
    """This repository implements CRUD operations"""

    def __init__(self, engine, db_session=db) -> None:
        """This initializes the session for database access"""
        self.db_session = db_session
        self.engine = engine

    def create_table(self):
        '''This method creates the tables in the database.'''
        Base.metadata.create_all(self.db_session)

    def get_all(self, model_name: str) -> list:
        """Returns a list of dictionaries representing all records of the given model."""
        # Assuming 'model_name' is a valid model class reference. If it's a string, you'll need to map it to a model class.
        model_class = self._get_model_class_by_name(model_name)  # You need to implement this method.
        query_result = self.db_session.query(model_class).all()
        data = [self._model_to_dict(instance) for instance in query_result]
        return data

    def _model_to_dict(self, instance):
        """Converts a SQLAlchemy model instance into a dictionary."""
        return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

    def _get_model_class_by_name(self, model_name):
        """Returns the model class based on the given model name."""
        if model_class is None:
            raise ValueError(f"Invalid model name: {model_name}")
        model_class = getattr(self.db_session, model_name, None)
        return model_class

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Retrieves a single object by the id"""
        model_class = self._get_model_class_by_name(model_name)
        return self.db_session.query(model_class).filter(model_class == obj_id).first()


    def reload(self) -> None:
        """Not implemented"""
        pass

    def save(self, obj: Base) -> None: #use this as example to fill the rest of methods
        """Saves object in table"""
        try:
            self.db_session.add(obj)
            self.db_session()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def update(self, obj: Base) -> Base | None:
        """This method saves an object and returns nothing"""
        try:
            self.db_session.commit()
            return obj
        except SQLAlchemyError:
            self.db_session.rollback()
            return None

    def delete(self, obj: Base) -> bool:
        """
            This method deletes an object and returns
            false if it did not work and true if it did.
        """
        try:
            self.db_session.delete(obj)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.db_session.rollback()
            return False
