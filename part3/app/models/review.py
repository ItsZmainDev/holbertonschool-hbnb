from app.models import BaseModel
from typing import TYPE_CHECKING
import uuid
from datetime import datetime
from app.extensions import db

if TYPE_CHECKING:
    from app.models import User
    from app.models import Place

class Review(BaseModel, db.Model):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
        db.CheckConstraint('length(text) > 0', name='text_not_empty'),
    )

    def __init__(self, text, rating, user, place):
        super().__init__()
        self._text = None
        self._rating = None
        self._user = None
        self._place = None

        self.text = text
        self.rating = rating
        self.user = user
        self.place = place
        self.user_id = user.id if user else None
        self.place_id = place.id if place else None

    # @property
    # def text(self):
    #     return self._text

    # @text.setter
    # def text(self, value):
    #     if not isinstance(value, str) or not value.strip():
    #         raise ValueError("Text must be a non-empty string")
    #     self._text = value.strip()

    # @property
    # def rating(self):
    #     return self._rating

    # @rating.setter
    # def rating(self, value):
    #     if not isinstance(value, int):
    #         raise TypeError("Rating must be an integer")
    #     if value < 1 or value > 5:
    #         raise ValueError("Rating must be between 1 and 5")
    #     self._rating = value

    # @property
    # def user(self):
    #     return self._user

    # @user.setter
    # def user(self, value):
    #     from app.models.user import User
    #     if not isinstance(value, User):
    #         raise TypeError("User must be an instance of User")
    #     if not hasattr(value, 'id') or not value.id:
    #         raise ValueError("User must have a valid id")
    #     self._user = value

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id
        }