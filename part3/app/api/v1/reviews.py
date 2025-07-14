from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.utils.auth_decorators import owner_or_admin_required

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data or not allowed')
    @jwt_required()
    def post(self):
        """Create a new review (authenticated user only)"""
        data = request.json
        current_user_id = get_jwt_identity()
        # Vérifier que le lieu existe
        place = facade.get_place(data["place_id"])
        if not place:
            api.abort(400, "Place not found")

        # L'utilisateur ne peut pas reviewer son propre lieu
        if place["owner_id"] == current_user_id:
            api.abort(400, "You cannot review your own place")

        # L'utilisateur ne peut pas reviewer deux fois le même lieu
        if facade.user_already_reviewed(current_user_id, data["place_id"]):
            api.abort(400, "You have already reviewed this place")

        # Injecter l'utilisateur dans la review
        data["user_id"] = current_user_id

        review = facade.create_review(data)
        if not review:
            api.abort(400, "Failed to create review")

        return review, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        return facade.get_all_reviews(), 200


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a single review by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review, 200

    @owner_or_admin_required
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Access denied')
    def put(self, review_id):
        """Update a review (Owner or Admin only)"""
        review_data = api.payload
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        updated_review = facade.update_review(review_id, review_data)

        return {'message': 'Review updated successfully'}, 200
    
    @owner_or_admin_required
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(403, 'Access denied')
    def delete(self, review_id):
        """Delete a review (Owner or Admin only)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            api.abort(404, 'Place not found')
        return reviews, 200