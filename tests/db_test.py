import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.persistence.db import DBRepository
from src.models.base import Base
from src.models.user import User
from src.models.amenity import Amenity
from src.models.review import Review
from src.models.place import Place
from src.models.city import City
from src.models.country import Country # Import your model

class TestDatabaseCRUD(unittest.TestCase):
    def setUp(self):
        # Setup in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
        self.db_repository = DBRepository(engine=self.engine, db_session=self.session)

    def test_create_entity(self):
        # Test creating an entity
        new_entity = self.db_repository.create(User, first_name="Test Name", last_name="stest", email="test3@test.com")
        self.session.commit()
        self.assertIsNotNone(new_entity.id)

    # Implement read, update, delete tests similarly

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

if __name__ == "__main__":
    unittest.main()
