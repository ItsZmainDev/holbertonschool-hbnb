from base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, description, place):
        super().__init__()
        self.name = name
        self.description = description
        self.place = place
