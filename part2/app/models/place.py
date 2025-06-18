from base_model import BaseModel
from user import User


class Place(BaseModel):
    def __init__(
        self, type, description, longitude, latitude,
        price_per_night, max_guests, is_available, owner
    ):
        super().__init__()
        self.type = type
        self.description = description
        self.longitude = longitude
        self.latitude = latitude
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.is_available = is_available
        self.owner: User = owner
        self.amenities = []

    def to_dict():
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'type': self.type,
            'description': self.description,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'is_available': self.is_available,
            'owner': self.owner,
            'amenities': self.amenities
        }
