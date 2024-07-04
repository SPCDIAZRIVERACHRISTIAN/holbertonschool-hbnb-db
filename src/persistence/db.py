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
from src.models import db
from sqlalchemy.exc import SQLAlchemyError
from src.models.country import Country


class DBRepository(Repository):
    """Dummy DB repository"""

    def __init__(self) -> None:
        """Initialize the DBRepository"""
        self.session = db.session
        self.reload()

    def get_all(self, model_name: str) -> list:
        """Get all objects of a given model from the database"""
        try:
            return self.session.query(model_name).all()
        except SQLAlchemyError:
            self.session.rollback()
            return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Get an object of a given model by its ID from the database"""
        try:
            return self.session.query(model_name).get(obj_id)
        except SQLAlchemyError:
            self.session.rollback()
            return None

    def reload(self) -> None:
        """Reload the database"""
        from utils.populate import populate_db
        populate_db(self)
        db.create_all()

    def save(self, obj: Base) -> None:
        """Save an object to the database"""
        try:
            self.session.add(obj)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()

    def update(self, obj: Base) -> Base | None:
        """Update an object in the database"""
        try:
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()

    def delete(self, obj: Base) -> bool:
        """Delete an object from the database"""
        try:
            self.session.delete(obj)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def get_by_code(self, model, code):
        return self.session.query(model).filter_by(code=code).first()
