from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from app.services import facade

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifiez d'abord si l'en-tête Authorization est présent
        auth_header = request.headers.get('Authorization')
        print(f"🔍 Authorization header: {auth_header}")  # Debug
        
        if not auth_header:
            print("❌ No Authorization header found")  # Debug
            return {'error': 'Token required'}, 401
            
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request()
            print("✅ JWT verification passed")  # Debug
        except Exception as e:
            print(f"❌ JWT verification failed: {e}")  # Debug
            return {'error': 'Token required'}, 401
        
        claims = get_jwt()
        current_user_id = get_jwt_identity()  # C'est maintenant une chaîne
        
        print(f"🔍 Current user ID: {current_user_id}")  # Debug
        print(f"🔍 JWT claims: {claims}")  # Debug
        
        if claims.get('is_admin'):
            print("✅ User is admin (from claims)")  # Debug
            return f(*args, **kwargs)
        
        user = facade.get_user(current_user_id)  # Utilise directement la chaîne
        if not user or not user.is_admin:
            print(f"❌ User not admin: {user}")  # Debug
            return {'error': 'Administrator access required'}, 403
        
        print("✅ User is admin (from database)")  # Debug
        return f(*args, **kwargs)
    
    return decorated_function

def owner_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request()
        except Exception as e:
            return {'error': 'Token required'}, 401
        
        current_user_id = get_jwt_identity()  # C'est maintenant une chaîne
        claims = get_jwt()
        
        if claims.get('is_admin'):
            return f(*args, **kwargs)
        
        current_user = facade.get_user(current_user_id)  # Utilise directement la chaîne
        if not current_user:
            return {'error': 'User not found'}, 404

        if current_user.is_admin:
            return f(*args, **kwargs)
        
        resource_id = kwargs.get('user_id') or kwargs.get('place_id') or kwargs.get('review_id')
        if resource_id:
            if 'user_id' in kwargs and kwargs['user_id'] == current_user_id:
                return f(*args, **kwargs)
            elif 'place_id' in kwargs:
                place = facade.get_place(kwargs['place_id'])
                if place and place.owner_id == current_user_id:
                    return f(*args, **kwargs)
            elif 'review_id' in kwargs:
                review = facade.get_review(kwargs['review_id'])
                if review and review.user_id == current_user_id:
                    return f(*args, **kwargs)
        
        return {'error': 'Access denied. You must be the owner or an administrator'}, 403
    
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request()
        except Exception as e:
            return {'error': 'Token required'}, 401
        
        return f(*args, **kwargs)
    
    return decorated_function