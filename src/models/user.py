"""
User related functionality
"""

from src.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    """User representation"""

    __tablename__ = 'Users'
    id = Column(String(156), unique=True, nullable=False primary_key=True)
    updated_at = Column(String(156))
    created_at = Column(String(156))
    email = Column(String(156), nullable=False unique=True)
    password = Column( nullable=False)#for later fixing
    is_admin = Column()#for later fixing
#use relationship to link different classes you can use as argument options backref="" to link it as a A.b and cascade= which lets you do different things that will affect both classes
    place = relationship("Place")
    amenity = relationship("Amenity")
    city = relationship("City")
    country = relationship("Country")

    def __init__(self, email: str, first_name: str, last_name: str, **kw):
        """Dummy init"""
        super().__init__(**kw)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(user: dict) -> "User":
        """Create a new user"""
        from src.persistence import repo

        users: list["User"] = User.get_all()

        for u in users:
            if u.email == user["email"]:
                raise ValueError("User already exists")

        new_user = User(**user)

        repo.save(new_user)

        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""
        from src.persistence import repo

        user: User | None = User.get(user_id)

        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        repo.update(user)

        return user
