from app.models import BaseModel
from typing import List, TYPE_CHECKING
import uuid
from datetime import datetime
from app.extensions import db

if TYPE_CHECKING:
    from app.models import User
    from app.models import Amenity

place_amenities = db.Table('place_amenities',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel, db.Model):
    __tablename__ = 'places'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price_per_night = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    reviews = db.relationship('Review', backref='place', lazy='dynamic')
    amenities = db.relationship('Amenity', secondary=place_amenities, backref='places')

    def __init__(
        self, type, title, description, longitude, latitude,
        price_per_night, max_guests, is_available, owner
    ):
        super().__init__()
        self.type = type
        self.title = title
        self.description = description
        self.longitude = longitude
        self.latitude = latitude
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.is_available = is_available
        self.owner: User = owner
        self.amenities: List[Amenity] = []

    # @property
    # def title(self):
    #     return self.__title

    # @title.setter
    # def title(self, value):
    #     if not isinstance(value, str):
    #         raise TypeError("Title must be a string")
    #     super().is_max_length('Title', value, 50)
    #     self.__title = value

    # @property
    # def price_per_night(self):
    #     return self.__price_per_night


    # @price_per_night.setter
    # def price_per_night(self, value):
    #     if not isinstance(value, float):
    #         raise TypeError("Price per night must be a float")
    #     if value < 0:
    #         raise ValueError("Price per night cannot be negative ")
    #     self.__price_per_night = value

    # @property
    # def longitude(self):
    #     return self.__longitude

    # @longitude.setter
    # def longitude(self, value):
    #     if not isinstance(value, float):
    #         raise TypeError("Longitude must be a float")
    #     if value < -180.0 or value > 180.0:
    #         raise ValueError("Longitude must be between -180.0 and 180.0")
    #     self.__longitude = value

    # @property
    # def latitude(self):
    #     return self.__latitude

    # @latitude.setter
    # def latitude(self, value):
    #     if not isinstance(value, float):
    #         raise TypeError("Latitude must be a float")
    #     if value < -90.0 or value > 90.0:
    #         raise ValueError("Latitude must be between -90.0 and 90.0")
    #     self.__latitude = value

    # @property
    # def owner(self):
    #     return self.__owner

    # @owner.setter
    # def owner(self, value):
    #     from app.models.user import User
    #     if not isinstance(value, User):
    #         raise TypeError("Owner must be an instance of User")
    #     if not hasattr(value, 'id') or value.id is None:
    #         raise ValueError("Owner must have a valid id")
    #     self.__owner = value

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'type': self.type,
            'title': self.title,
            'description': self.description,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'is_available': self.is_available,
            'owner_id': self.owner.id if self.owner else None,
            'amenities': [amenity.id for amenity in self.amenities],
        }
