from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.utils.auth_decorators import owner_or_admin_required, login_required 

api = Namespace('places', description='Place operations')

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price_per_night': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews'),
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        data = api.payload
        if not data or 'title' not in data or 'price_per_night' not in data:
            api.abort(400, 'Invalid input data')
        place = facade.create_place(data)
        return place, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return places, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        return place, 200

    @owner_or_admin_required
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Access denied')
    def put(self, place_id):
        """Update a place's information (Owner or Admin only)"""
        place_data = api.payload
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        updated_place = facade.update_place(place_id, place_data)
        return {'message': 'Place updated successfully'}, 200

    @owner_or_admin_required
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Access denied')
    def delete(self, place_id):
        """Delete a place (Owner or Admin only)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200