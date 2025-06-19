import re
from base_model import BaseModel
from place import Place
from review import Review


class User(BaseModel):
    first_name: str = CharField(max_length=50)
    last_name: str = CharField(max_length=50)
    phone_number: str = CharField(max_length=15, null=True)
    profile_picture: str = CharField(max_length=255, null=True)
    address: str = CharField(max_length=255, null=True)
    email: str = CharField(max_length=100, unique=True)
    password: str = CharField(max_length=128)
    is_admin: bool = BooleanField(default=False)
    is_owner: bool = BooleanField(default=False)
    places: List[Place] = ForeignKeyField(Place, backref='users', null=True)
    reviews: List[Review] = ForeignKeyField(Review, backref='users', null=True)

    def __init__(
        self, first_name, last_name, phone_number, profile_picture,
        address, email, password, is_admin=False, is_owner=False
    ):
        super().__init__()
        
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.profile_picture = profile_picture
        self.address = address
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_owner = is_owner
        self.places: List[Place] = []
        self.reviews: List[Review] = []

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'profile_picture': self.profile_picture,
            'address': self.address,
            'email': self.email,
            'password': self.password,
            'is_admin': self.is_admin,
            'is_owner': self.is_owner,
            'places': [place.id for place in self.places],
            'reviews': [review.id for review in self.reviews]
        }
