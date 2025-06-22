from app.models.amenity import Amenity

class AmenityRepository:
    _storage = {}

    def save(self, amenity):
        self._storage[amenity.id] = amenity

    def get_by_id(self, amenity_id):
        return self._storage.get(amenity_id)

    def get_all(self):
        return list(self._storage.values())
