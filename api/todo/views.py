from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource,Namespace,fields
from ..models.users import User
from ..models.resp_data import RespSuccessData, RespErrorData
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
    'TodoData',{
        'id':fields.Integer(required=True,decription='Todo Unique id'),
        'name':fields.String(required=True, description="Todo Name"),
        'description':fields.String(required=False, description="Todo Description"),
        'start_date':fields.DateTime(required=False, description="Todo start date"),
        'status':fields.String(required=True, description='Todo Status', enum=["created","started","completed","expired","unknown"]),
        'category_id':fields.Integer(required=True, description="Category Id") 
    }
)

todo_resp_model = todo_name_space.model(
    'TodoResp',{
        'status':fields.Boolean(required=True, description='Status'),
        'message':fields.String(required=True, description='Response status message'),
        'data':fields.Nested(todo_resp_data)
    }
)

todo_get_all_respmodel = todo_name_space.model(
    'TodoRespGet', {
        'status':fields.Boolean(required=True, description='Status'),
        'message':fields.String(required=True, description='Response status message'),
        'data':fields.List(fields.Nested(todo_resp_data))
    }
)

@todo_name_space.route('/')
class Tdodo(Resource):
    @todo_name_space.marshal_with(todo_get_all_respmodel)
    @jwt_required()
    def get(self):
        user_name = get_jwt_identity()
        current_user = User.query.filter_by(user_name = user_name).first()
        if(current_user is not None):
            return RespSuccessData(status=True, message="Success",data=current_user.todos), HTTPStatus.OK
        
        resp_data = {
            "status":True,
            "message":"Could not complete the request"
        }
        return resp_data, HTTPStatus.OK
   
    @todo_name_space.expect(todo_req_model)
    @todo_name_space.marshal_with(todo_resp_model)
    @jwt_required()
    def post(self):
        user_name = get_jwt_identity()
        current_user = User.query.filter_by(user_name = user_name).first()
        if(current_user is not None):
            data = todo_name_space.payload
            name = data.get("name")
            description = data.get('description')
            start_date = datetime.fromtimestamp(data.get('start_date')/1000)
        
            status = ToDoStatus(data.get('status').upper())
            category_id = data.get('category_id')
            todo = Todo(name=name,description=description,start_date=start_date,status=status,category_id=category_id,user_id=current_user.id)
            todo.save()
            resp = RespSuccessData(status=True,message ="Successfully added", data=todo)
            return resp, HTTPStatus.CREATED
        else:
            resp = RespSuccessData(status=False, message="Could not found the user")
            return resp, HTTPStatus.BAD_REQUEST


@todo_name_space.route('/<int:todo_id>')
class GetOrUpdateTodo(Resource):

    @todo_name_space.marshal_with(todo_resp_model)
    @jwt_required()
    def get(self, todo_id):
        user_name = get_jwt_identity()
        current_user = User.query.filter_by(user_name=user_name).first()
        print("\nTdod Id:", todo_id)
        todo = list(filter(lambda todo: todo.id == todo_id, current_user.todos))
        print("\nTodo Data:", todo)
        if len(todo)> 0:
            return RespSuccessData(status=True,message="Success",data=todo[0]), HTTPStatus.OK
        return  {
            'status':False,
            'message':"Todo data not found"
        }
    @todo_name_space.expect(todo_req_model)
    @todo_name_space.marshal_with(todo_resp_model)
    @jwt_required()
    def put(self, todo_id):
        user_name = get_jwt_identity()
        current_user = User.query.filter_by(user_name= user_name).first()
        todo_req = todo_name_space.payload
        if(current_user is not None):
            todo = Todo.query.filter_by(id = todo_id).first()
            if(todo is not None and todo.user_id == current_user.id):
                todo.name = todo_req['name']
                todo.description = todo_req['description']
                todo.status = ToDoStatus(todo_req['status'].upper())
                todo.category_id = todo_req['category_id']
                todo.save()
                return RespSuccessData(status=True,message="Success",data=todo), HTTPStatus.OK
        return RespErrorData(status=False,message="Failed"), HTTPStatus.BAD_REQUEST
    @jwt_required()
    def delete(self, todo_id):
        user_name = get_jwt_identity()
        current_user = User.query.filter_by(user_name= user_name).first()
        todo_req = list(filter(lambda todo: todo.id == todo_id, current_user.todos))
        if len(todo_req) > 0 :
            todo_req[0].delete()
            return {
                'status':True,
                'message':'Success'
            }, HTTPStatus.OK
        return {
                'status':False,
                'message':'Failed to delete'
            }, HTTPStatus.BAD_REQUEST
    def patch(self, todo_id):
        pass

def id_filer(todo_id, todo):
    if todo_id == todo.id:
        return True
    else:
        return False






