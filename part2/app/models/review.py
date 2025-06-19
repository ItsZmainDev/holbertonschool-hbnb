from base_model import BaseModel
from user import User
from place import Place


class Review(BaseModel):
    text: str = CharField()
    rating: int = CharField(max_length=5, default=1)
    user: User = ForeignKeyField(User, backref='reviews')
    place: Place = ForeignKeyField(Place, backref='reviews')

    def __init__(self, text, rating=1, user, owner, place):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user: User = user
        self.place: Place = place

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'text': self.text,
            'rating': self.rating,
            'user': self.user,
            'place': self.place
        }
