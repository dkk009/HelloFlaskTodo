from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource,Namespace,fields
from ..models.users import User
from ..models.resp_data import RespData
from ..models.todo import Todo
from flask import request
from http import HTTPStatus
from datetime import datetime
from ..models.todo import ToDoStatus
todo_name_space = Namespace(name="todo", description='Todo Name space')
todo_req_model = todo_name_space.model(
    'Todo',{
        'name':fields.String(required=True, description="Todo Name"),
        'description':fields.String(required=False, description="Todo Description"),
        'start_date':fields.Integer(required=False, description="Todo start date"),
        'status':fields.String(required=True, description='Todo Status', enum=["created","started","completed","expired","unknown"]),
        'category_id':fields.Integer(required=True, description="Category Id"),
        
    }
)
todo_resp_data = todo_name_space.model(
    'Todo',{
        'name':fields.String(required=True, description="Todo Name"),
        'description':fields.String(required=False, description="Todo Description"),
        'start_date':fields.DateTime(required=False, description="Todo start date"),
        'status':fields.String(required=True, description='Todo Status', enum=["created","started","completed","expired","unknown"]),
        'category_id':fields.Integer(required=True, description="Category Id"),
        
    }
)
todo_resp_model = todo_name_space.model(
    'TodoResp',{
        'status':fields.Boolean(required=True, description='Status'),
        'message':fields.String(required=True, description='Response status message'),
        'data':fields.Nested(todo_resp_data)
    }
)

@todo_name_space.route('/')
class Tdodo(Resource):
    @jwt_required()
    def get(self):
        return {"message":"Hello Tdoo"}
   
    @todo_name_space.expect(todo_req_model)
    @todo_name_space.marshal_with(todo_resp_model)
    @jwt_required()
    def post(self):
        user_name = get_jwt_identity()
        current_user = User.query.filter_by(user_name = user_name).first()
        print("I am in todo creation")
        if(current_user is not None):
            data = request.get_json()
            name = data.get("name")
            description = data.get('description')
            start_date = datetime.fromtimestamp(data.get('start_date')/1000)
        
            status = ToDoStatus(data.get('status'))
            category_id = data.get('category_id')
            print("Current User Id:", current_user.id)
            todo = Todo(name=name,description=description,start_date=start_date,status=status,category_id=category_id,user_id=current_user.id)
            todo.save()
            resp = RespData(status=True,message ="Successfully added", data=todo)
            return resp, HTTPStatus.CREATED
        else:
            resp = RespData(status=False, message="Could not found the user")
            return resp, HTTPStatus.BAD_REQUEST


@todo_name_space.route('/<int:todo_id>')
class GetOrUpdateTodo(Resource):
    def get(self, todo_id):
        pass
    def put(self, todo_id):
        pass
    def delete(self, todo_id):
        pass
    def patch(self, todo_id):
        pass

