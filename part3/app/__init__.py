from flask import Flask
from app.extensions import db
from app.extensions import jwt
from app.extensions import bcrypt
from flask_restx import Api

# Import des namespaces API
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.test import api as test_ns

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
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

    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Tables recreated successfully!")

    return app
