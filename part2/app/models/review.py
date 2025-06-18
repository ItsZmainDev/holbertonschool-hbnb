from base_model import BaseModel
from user import User
from place import Place


class Review(BaseModel):
    def __init__(self, text, rating, user, owner, place):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user: User = user
        self.owner: User = owner
        self.place: Place = place

    def to_dict():
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'text': self.text,
            'rating': self.rating,
            'owner': self.owner
            'place': self.place
        }
