from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_amenity(self, amenity_data):
        new_amenity = Amenity(
            id=str(uuid.uuid4()),
            name=amenity_data['name'],
            description=amenity_data.get('description', ''),
            place=None
        )
        self.amenity_repo.add(new_amenity.id, new_amenity)
        return new_amenity.to_dict()

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            return amenity.to_dict()
        return None

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False
        amenity.name = amenity_data.get('name', amenity.name)
        amenity.description = amenity_data.get('description', amenity.description)
        self.amenity_repo.update(amenity_id, amenity)
        return True