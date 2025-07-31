from flask import Flask
from app.extensions import db
from app.extensions import jwt
from app.extensions import bcrypt
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Import des namespaces API
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.test import api as test_ns

def create_app(config_class):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
        }
    }
    
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        authorizations=authorizations,
        security='Bearer Auth',
        doc='/api/v1/'
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(test_ns, path='/api/v1/test')

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired'}, 401

    def create_default_admin():
        """Create a default admin user if it doesn't exist"""
        from app.services.facade import HBnBFacade
        facade = HBnBFacade()
        
        admin_email = 'test@hbnb.io'
        existing_admin = facade.get_user_by_email(admin_email)
        
        if not existing_admin:
            admin_data = {
                'first_name': 'Admin',
                'last_name': 'HBnB',
                'phone_number': '+1234567890',
                'email': admin_email,
                'password': 'admin1234',
                'is_admin': True
            }
            
            admin_user = facade.create_user(admin_data)
            print(f"User created successfully: {admin_user.email}")
        else:
            print(f"User already exists: {admin_email}")

    with app.app_context():
        db.create_all()
        print("Tables recreated successfully!")
        create_default_admin()

    return app
