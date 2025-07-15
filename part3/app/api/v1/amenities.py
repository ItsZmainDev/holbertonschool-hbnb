from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.utils.auth_decorators import admin_required, owner_or_admin_required, login_required

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, description='Description of the amenity'),
})

@api.route('/')
class AmenityList(Resource):
    @admin_required
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Administrator access required')
    def post(self):
        """Create a new amenity (Admin only)"""
        amenity_data = api.payload
        place_id = request.args.get('place_id')
        
        if place_id:
            try:
                new_amenity = facade.create_amenity_for_place(amenity_data, place_id)
                return {'id': new_amenity.id, 'name': new_amenity.name}, 201
            except ValueError as e:
                return {'error': str(e)}, 404
        else:
            new_amenity = facade.create_amenity(amenity_data)
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name, 'description': amenity.description} for amenity in amenities], 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @admin_required
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Administrator access required')
    def put(self, amenity_id):
        """Update an amenity's information (Admin only)"""
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        return {'message': 'Amenity updated successfully'}, 200
