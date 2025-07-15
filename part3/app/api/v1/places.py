from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services import facade
from app.utils.auth_decorators import owner_or_admin_required, login_required 

api = Namespace('places', description='Place operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity'),
})

place_model = api.model('Place', {
    'type': fields.String(required=True, description='Type of the place (e.g., apartment, house)'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price_per_night': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'max_guests': fields.Integer(required=True, description='Maximum number of guests'),
    'is_available': fields.Boolean(description='Availability status', default=True),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place (authenticated only)"""
        data = request.get_json()
        if not data or 'title' not in data or 'price_per_night' not in data:
            api.abort(400, 'Invalid input data')
        required_fields = ['type', 'title', 'price_per_night', 'latitude', 'longitude', 'max_guests']
        for field in required_fields:
            if field not in data:
                api.abort(400, f'Missing required field: {field}')

        current_user_id = get_jwt_identity()
        data['owner_id'] = current_user_id

        if 'is_available' not in data:
            data['is_available'] = True

        place = facade.create_place(data)
        return place, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places (public)"""
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
    @api.response(403, 'Unauthorized action')
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

@api.route('/<string:place_id>/amenities')
class PlaceAmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created for place')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    def post(self, place_id):
        """Create a new amenity for a specific place"""
        amenity_data = request.get_json()
        if not amenity_data or 'name' not in amenity_data:
            api.abort(400, 'Invalid input data')
        
        try:
            amenity = facade.create_amenity_for_place(amenity_data, place_id)
            return {'id': amenity.id, 'name': amenity.name, 'description': amenity.description}, 201
        except ValueError as e:
            api.abort(404, str(e))

    @api.response(200, 'List of amenities for place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all amenities for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        
        amenities = facade.get_amenities_by_place(place_id)
        return amenities, 200