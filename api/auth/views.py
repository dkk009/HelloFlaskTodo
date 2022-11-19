from flask_restx import Namespace, Resource,fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
import json

auth_name_space = Namespace(name='auth', description='Auth name space')
sign_up_model = auth_name_space.model(
    'User',{
        'email':fields.String(required=True, description="An Email"),
        'password':fields.String(required=True, description="Authentication password"),
        'name':fields.String(required=True, description="Name field")
    }
)

login_model = auth_name_space.model(
    'Login',{
        'user_name':fields.String(required=True, description="User name"),
        'password':fields.String(required=True, description="User password")
    }
)

@auth_name_space.route('/login')
class Authentication(Resource):
    @auth_name_space.expect(login_model)
    def post(self):
        data = request.get_json()
        user_name = data.get('user_name')
        password = data.get('password')
        current_user = User.query.filter_by(user_name = user_name).first()
        if current_user is not None  and check_password_hash(current_user.password, password):
            access_token = create_access_token(identity=user_name)
            refresh_token= create_refresh_token(identity=user_name)
            response={
                'message':'Authenticated successfully',
                'access_token':access_token,
                'refresh_token':refresh_token,
                'status':True
            }
            return response, HTTPStatus.OK
        response={
            "message":"User not found"
        }
        return response, HTTPStatus.BAD_REQUEST

@auth_name_space.route('/register')
class RegisterNewUser(Resource):
    @auth_name_space.expect(sign_up_model)
    def post(self):
        data = request.get_json()
        existing_user = User.query.filter_by(user_name = data.get('email')).first()
        if existing_user is None:
            new_user = User(
                email=data.get('email'),
                password=generate_password_hash(data.get('password')),
                name=data.get('name')
            )
            new_user.save()
            access_token = create_access_token(identity=new_user.email)
            refresh_token = create_refresh_token(identity=new_user.email)
            response = {
                'message':'Successfully created account',
                'access_token':access_token,
                'refresh_token':refresh_token,
                'data': new_user.as_dict()

            }
            return response, HTTPStatus.CREATED
        response = {
            "message":"User existing '{existing_user.user_name}'"
        }
        return response, HTTPStatus.BAD_REQUEST

@auth_name_space.route('/refresh_token')
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_name = get_jwt_identity()
        access_token = create_access_token(identity=user_name)
        refresh_token = create_refresh_token(identity=user_name)
        response = {
            'status':True,
            'access_token':access_token,
            'refresh_token':refresh_token
        }
        return response, HTTPStatus.OK
