from base_model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from place import Place


class Amenity(BaseModel):
    def __init__(self, name, description, place):
        super().__init__()
        self.name = name
        self.description = description
        self.place: Place = place

    @property
    def name(self):
        self.__name = self.name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        super().is_max_length("Name", value, 50)
        self.__name = self.name

    @property
    def place(self):
        self.__place = self.place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise TypeError("Place must be an instance of Place")
        if not hasattr(value, 'id') or value.id is None:
            raise ValueError("Place must have a valid id")
        self.__place = value

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name': self.name,
            'description': self.description,
            'place': self.place
        }
