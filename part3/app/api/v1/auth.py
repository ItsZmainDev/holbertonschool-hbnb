from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask import request
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class LoginResource(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return a JWT token"""
        data = request.get_json()

        user = facade.get_user_by_email(data['email'])
        print(user)
        if not user or not user.verify_password(data['password']):
            return {'error': 'Invalid credentials'}, 401

        token = create_access_token(
            identity=str(user.id),
            additional_claims={'id': user.id, 'is_admin': user.is_admin}
        )
        return {'access_token': token}, 200