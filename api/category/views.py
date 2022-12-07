from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, Namespace, fields
from flask import request 
from ..models.category import Category
from ..models.users import User
from ..models.resp_data import RespSuccessData
from http import HTTPStatus
import json
category_name_space = Namespace(name='category', description="Category name space")
category_req_model = category_name_space.model(
    'category',{
        'name':fields.String(required=True, description="Category name"),
        'description':fields.String(required=True, description="Category description")
    }
)
category_model = category_name_space.model(
    'data',{
         'id':fields.Integer(required=True, description="Category id"),
         'name':fields.String(required=True, description="Category name"),
         'description':fields.String(required=False, description='Category descritpion'),
         'created_date':fields.String(required=True,description='Category created date'),
    }
)
category_resp_model = category_name_space.model(
    'respdata',{
        'status':fields.Boolean(required=True, description="Status"),
        'message':fields.String(required=True, description='Response status message'),
        'data':fields.List(fields.Nested(category_model))
    }
)
category_creation_resp_model = category_name_space.model(
    'respdata',{
        'status': fields.Boolean(required=True, description= "Status"),
        'message': fields.String(required=True, description='Response message'),
        'data':fields.Nested(category_model)
    }
)


@category_name_space.route("/")
class CreateOrGetCategory(Resource):
    @category_name_space.expect(category_req_model)
    @category_name_space.marshal_with(category_creation_resp_model)
    @jwt_required()
    def post(self):
        user_name = get_jwt_identity()
        current_user = User.query.filter_by(user_name = user_name).first()
        data = request.get_json()
        category_name = data.get('name')
        category_description = data.get('description')
        print('categorytName:', category_name)
        print('descirption:', category_description)
        if current_user is not None and category_name is not None:
            category = Category(name=category_name, description= category_description, user_id= current_user.id)
            category.save()
            resp = RespSuccessData(status=True,message='Success',data=category)
            return resp, HTTPStatus.CREATED
        resp = {
            'message':'Category name is not found in request',
            'status':False
        }
        return resp, HTTPStatus.BAD_REQUEST

    @jwt_required()
    @category_name_space.marshal_with(category_resp_model)
    def get(self):
        user_name = get_jwt_identity()
        current_user = User.query.filter_by(user_name = user_name).first()
        if current_user is not None:
            categoryList = current_user.categories
            response = RespSuccessData(status=True,message='Success',data=categoryList)
            return response, HTTPStatus.OK
        resp = {
            'message':'Category name is not fond in request',
            'status':False
        }
        return resp, HTTPStatus.BAD_REQUEST

@category_name_space.route("/<int:category_id>")
class GetOrUpdateCategory(Resource):
    def get(self, category_id):
        pass
    def put(self, category_id):
        pass
    def delete(self, category_id):
        pass
