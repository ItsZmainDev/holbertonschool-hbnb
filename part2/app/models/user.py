from base_model import BaseModel


class User(BaseModel):
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
        self.places = []
        self.reviews = []

    def to_dict():
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number
            'profile_picture': self.profile_picture,
            'address': self.address
            'email': self.email
            'password': self.password
            'is_admin': self.is_admin
            'is_owner': self.is_owner
            'places': self.places
            'reviews': self.reviews
        }
