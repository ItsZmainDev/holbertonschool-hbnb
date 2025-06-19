from base_model import BaseModel
from user import User


class Place(BaseModel):
    def __init__(
        self, type, title, description, longitude, latitude,
        price_per_night, max_guests, is_available, owner
    ):
        super().__init__()

        if not title:
            return ValueError("title is not defined")

        if price_per_night < 0:
            return ValueError("price_per_night can't be under 0")

        if latitude < -90.0 or latitude > 90.0:
            ValueError("latitude must be between -90.0 and 90.0")

        if longitude < -180.0 or longitude > 180.0:
            ValueError("longitude must be between -180.0 and 180.0")

        if not owner or not isinstance(owner, User):
            return ValueError(
                "owner must be defined and must be an instance of User"
            )

        self.type = type
        self.title = title
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
            'title': self.title,
            'description': self.description,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'is_available': self.is_available,
            'owner': self.owner,
            'amenities': self.amenities
        }
