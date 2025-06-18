from base_model import BaseModel
from place import Place


class Amenity(BaseModel):
    def __init__(self, name, description, place):
        super().__init__()
        self.name = name
        self.description = description
        self.place: Place = place

    def to_dict():
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name': self.name,
            'description': self.description,
            'place': self.place
        }
