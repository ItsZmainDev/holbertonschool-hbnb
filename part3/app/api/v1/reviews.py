from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

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
        current_user = get_jwt_identity()
        user_id = current_user["id"]

        # Vérifier le lieu
        place = facade.get_place(data["place_id"])
        if not place:
            api.abort(400, "Place not found")

        # L'utilisateur ne peut pas reviewer son propre lieu
        if place["user_id"] == user_id:
            api.abort(400, "You cannot review your own place")

        # L'utilisateur ne peut pas reviewer deux fois le même lieu
        if facade.user_already_reviewed(user_id, data["place_id"]):
            api.abort(400, "You have already reviewed this place")

        # Ajouter le user_id dans la data
        data["user_id"] = user_id

        review = facade.create_review(data)
        if not review:
            api.abort(400, "Failed to create review")

        return review, 201