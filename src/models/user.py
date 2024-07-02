"""
User related functionality
"""

from flask import app
from . import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User(db.Model):
    """User representation"""

    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(36), nullable=False)
    last_name = db.Column(db.String(36), nullable=False)

    places = db.relationship("Place", back_populates='host')
    reviews = db.relationship("Review", back_populates='user')


    def __init__(self, email: str, password: str, is_admin: bool, first_name: str, last_name: str, **kw):
        """Dummy init"""
        super().__init__(**kw)
        self.email = email
        self.password = password
        self.is_admin = is_admin
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
            "password": self.password,
            "is_admin": self.is_admin,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

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
        if repo.save(new_user) == True:
            print('user added')
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
        if "password" in data:
            user.password = data["password"]
        if "is_admin" in data:
            user.is_admin = data["is_admin"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        repo.update(user)

        return user
