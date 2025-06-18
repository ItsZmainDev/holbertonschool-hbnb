from base_model import BaseModel


class Place(BaseModel):
    def __init__(
        self, type, description, longitude, latitude,
        price_per_night, max_guests, is_available
    ):
        super().__init__()
        self.type = type
        self.description = description
        self.longitude = longitude
        self.latitude = latitude
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.is_available = is_available
        self.amenities = []
