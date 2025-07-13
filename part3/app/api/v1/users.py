from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.utils.auth_decorators import admin_required, owner_or_admin_required, login_required

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'phone_number': fields.String(required=True, description="Phone number of the user"),
    'email': fields.String(required=True, description='The email of the user'),
    'password': fields.String(required=True, description='The password of the user'),
    'address': fields.String(required=False, description='The address of the user'),
    'profile_picture': fields.String(required=False, description='The profile picture of the user')
})

@api.route('/')
class UserList(Resource):
    @admin_required
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)

        if 'password' in user_data:
            new_user.hash_password(user_data['password'])

        return {'id': new_user.id, 'message': 'User successfully created'}, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve the list of users"""
        users = facade.get_all_users()
        return [{
            'id': user.id, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email,
            'phone_number': getattr(user, 'phone_number', None),
            'address': getattr(user, 'address', None),
            'profile_picture': getattr(user, 'profile_picture', None)
        } for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email,
            'phone_number': getattr(user, 'phone_number', None),
            'address': getattr(user, 'address', None),
            'profile_picture': getattr(user, 'profile_picture', None)
        }, 200

    @owner_or_admin_required
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details by ID"""
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        if 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}, 400
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'Invalid input data'}, 400
        return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200
