from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

    def create_place(self, place_data):
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_data in place_data['amenities']:
                # Si c'est juste un ID (string)
                if isinstance(amenity_data, str):
                    amenity = self.amenity_repo.get(amenity_data)
                    if amenity:
                        amenities.append(amenity)
                elif isinstance(amenity_data, dict) and 'id' in amenity_data:
                    amenity = self.amenity_repo.get(amenity_data['id'])
                    if amenity:
                        amenities.append(amenity)
        
        place_data_clean = place_data.copy()
        if 'amenities' in place_data_clean:
            del place_data_clean['amenities']

        place = Place(
            type=place_data_clean['type'],
            title=place_data_clean['title'],
            description=place_data_clean.get('description', ''),
            longitude=place_data_clean['longitude'],
            latitude=place_data_clean['latitude'],
            price_per_night=place_data_clean['price_per_night'],
            max_guests=place_data_clean['max_guests'],
            is_available=place_data_clean.get('is_available', True),
            owner=owner
        )

        place.amenities = amenities

        self.place_repo.add(place)
        return place.to_dict()

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            return place.to_dict()
        return None

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        # Traiter les amenities si présents
        if 'amenities' in place_data and place_data['amenities']:
            amenities = []
            for amenity_data in place_data['amenities']:
                if isinstance(amenity_data, str):
                    amenity = self.amenity_repo.get(amenity_data)
                    if amenity:
                        amenities.append(amenity)
                elif isinstance(amenity_data, dict) and 'id' in amenity_data:
                    amenity = self.amenity_repo.get(amenity_data['id'])
                    if amenity:
                        amenities.append(amenity)
            place.amenities = amenities
            # Supprimer les amenities des données avant update
            place_data = place_data.copy()
            del place_data['amenities']
        
        return self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # ===== REVIEW METHODS =====
    def create_review(self, review_data):
        user = self.user_repo.get(review_data.get("user_id"))
        place = self.place_repo.get(review_data.get("place_id"))

        if not user or not place:
            raise ValueError("User or Place not found")

        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            user=user,
            place=place
        )
        self.review_repo.add(review)
        return review.to_dict()

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            return review.to_dict()
        return None

    def get_all_reviews(self):
        return [r.to_dict() for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_all()
        return [r.to_dict() for r in reviews if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False

    def user_already_reviewed(self, user_id, place_id):
        """Check if a user has already reviewed a place"""
        reviews = self.review_repo.get_all()
        for review in reviews:
            if review.user_id == user_id and review.place_id == place_id:
                return True
        return False