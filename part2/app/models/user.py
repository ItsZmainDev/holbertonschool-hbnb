from base_model import BaseModel


class User(BaseModel):
    def __init__(
        self, first_name, last_name, phone_number, profile_picture,
        address, email, password, isAdmin=False, isOwner=False
    ):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.profile_picture = profile_picture
        self.address = address
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        self.isOwner = isOwner
        self.places = []
        self.reviews = []
