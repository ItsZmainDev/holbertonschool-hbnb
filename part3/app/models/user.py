import re
from app.models import BaseModel
from typing import List, TYPE_CHECKING
from app.extensions import db
from app.extensions import bcrypt
import uuid
from datetime import datetime

if TYPE_CHECKING:
    from app.models.place import Place
    from app.models.review import Review


class User(BaseModel, db.Model):
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_owner = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relations
    places = db.relationship('Place', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    emails = set()

    def __init__(
        self, first_name, last_name, phone_number, email, password, address=None, profile_picture=None, is_admin=False, is_owner=False
    ):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.profile_picture = profile_picture
        self.address = address
        self.email = email
        # self.password = password
        if password:
            self.hash_password(password)
        else:
            self.password = password

        self.is_admin = is_admin
        self.is_owner = is_owner
        self.places: List[Place] = []
        self.reviews: List[Review] = []

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        print(f"Verifying password for user {self.email}")
        return bcrypt.check_password_hash(self.password, password)

    # @property
    # def is_admin(self):
    #     return self.__is_admin

    # @is_admin.setter
    # def is_admin(self, value):
    #     if not isinstance(value, bool):
    #         raise TypeError("Is Admin must be a boolean")
    #     self.__is_admin = value

    # @property
    # def first_name(self):
    #     return self.__first_name

    # @first_name.setter
    # def first_name(self, value):
    #     if not isinstance(value, str):
    #         raise TypeError("First name must be a string")
    #     super().is_max_length('First name', value, 50)
    #     self.__first_name = value

    # @property
    # def last_name(self):
    #     return self.__last_name

    # @last_name.setter
    # def last_name(self, value):
    #     if not isinstance(value, str):
    #         raise TypeError("Last name must be a string")
    #     super().is_max_length('Last name', value, 50)
    #     self.__last_name = value

    # @property
    # def email(self):
    #     return self.__email

    # @email.setter
    # def email(self, value):
    #     if not isinstance(value, str):
    #         raise TypeError("Email must be a string")
    #     if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
    #         raise ValueError("Invalid email format")
    #     if value in User.emails:
    #         raise ValueError("Email already exists")
    #     if hasattr(self, "_User__email"):
    #         User.emails.discard(self.__email)
    #     self.__email = value
    #     User.emails.add(value)

    # @property
    # def is_admin(self):
    #     return self.__is_admin

    # @is_admin.setter
    # def is_admin(self, value):
    #     if not isinstance(value, bool):
    #         raise TypeError("Is Admin must be a boolean")
    #     self.__is_admin = value
    
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'profile_picture': self.profile_picture,
            'address': self.address,
            'email': self.email,
            'password': self.password,
            'is_admin': self.is_admin,
            'is_owner': self.is_owner,
            'places': [place.id for place in self.places],
            'reviews': [review.id for review in self.reviews],
        }
