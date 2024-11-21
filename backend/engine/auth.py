from functools import wraps
from flask_restful import Resource
from flask import request, jsonify
import jwt
import datetime
from .models import User, Sponsor
from .config import Config

def create_jwt_token(user):
    try:
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        secret_key = Config.SECRET_KEY
        return jwt.encode(payload, secret_key, algorithm='HS256')
    except Exception as e:
        print(f"error creating jwt token: {str(e)}")
        return None
    
def token_required(roles=[]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header:
                try:
                    token = auth_header.split(' ')[1]
                    payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                    user_id = payload.get('user_id')
                    
                    if not user_id:
                        raise ValueError("User ID missing in token payload")
                    
                    user = User.query.get(user_id)
                    if not user:
                        return jsonify({'message': 'User not found'}), 404
                    
                    if roles and user.role_id not in roles:
                        return jsonify({'message': 'Access denied'}), 403
                    
                    request.user = user
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError) as e:
                    return jsonify({'message': f'Token error: {str(e)}'}), 401
            else:
                return jsonify({'message': 'Token is missing'}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator

import logging

logging.basicConfig(level=logging.DEBUG)
class AuthResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            print(data)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return jsonify({'status': False, 'error': 'Username and password are required'}), 400

            sponsor = Sponsor.query.filter_by(sponsor_name=username).first()
            if sponsor:
                return jsonify({'status': False, 'error': 'Username exists in Sponsor table. Please use a valid User account.'}), 400

            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                access_token = create_jwt_token(user)
                response_data = {
                    'status': True,
                    'role_id': user.role_id,
                    'username': user.username,
                    'access_token': access_token,
                    'is_banned': user.is_banned
                }
                logging.debug(f'Response Data: {response_data}')
                return jsonify(response_data)
            else:
                return jsonify({'status': False, 'error': 'Invalid username or password'}), 400

        except Exception as e:
            logging.error(f'Exception occurred: {e}')
            return jsonify({'status': False, 'error': 'Internal server error'}), 500
    

    @token_required(roles=[1, 2])
    def get(self):
        try:
            user = request.user
            return jsonify({'message': f'Welcome {user.username}!'}), 200
        except Exception as e:
            logging.error(f'Exception occurred: {e}')
            return jsonify({'status': False, 'error': 'Internal server error'}), 500
