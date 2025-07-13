from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('test', description='Protected test routes')

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        return {
            "message": f"Access granted for user {identity['id']}",
            "admin": identity['is_admin']
        }, 200
