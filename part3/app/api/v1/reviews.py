from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.utils.auth_decorators import owner_or_admin_required

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        data = request.json
        review = facade.create_review(data)
        if not review:
            api.abort(400, 'Invalid input data or related user/place not found')
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
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review, 200

    @owner_or_admin_required
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
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
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            api.abort(404, 'Place not found')
        return reviews, 200
