from base_model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user import User
    from place import Place


class Review(BaseModel):
    def __init__(self, text, rating, user, owner, place):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user: User = user
        self.place: Place = place

    @property
    def text(self):
        self.__text = self.text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        self.__text = value

    @property
    def rating(self):
        self.__rating = self.rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be a integer")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        self.__rating = value

    @property
    def user(self):
        self.__user = self.user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise TypeError("User must be an instance of User")
        if not hasattr(value, 'id') or value.id is None:
            raise ValueError("User must have a valid id")
        self.__user = value

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
            'text': self.text,
            'rating': self.rating,
            'user': self.user,
            'place': self.place
        }
