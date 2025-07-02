from app.models import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Place

class Amenity(BaseModel):
    def __init__(self, name, description=None, place=None, id=None):
        super().__init__()
        if id is not None:
            self.id = id
        self.name = name
        self.description = description
        self.place = place

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        super().is_max_length("Name", value, 50)
        self.__name = value
    
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'name': self.name,
            'description': self.description,
            'place': self.place
        }
