from flask_jwt_extended import jwt_required
from flask_restx import Resource,Namespace,fields

todo_name_space = Namespace(name="todo", description='Todo Name space')
todo_model = todo_name_space.model(
    'Todo',{
        'name':fields.String(required=True, description="Todo Name"),
        'description':fields.String(required=False, description="Todo Description"),
        'start_date':fields.DateTime(required=False, description="Todo start date"),
        'created_date':fields.DateTime(required=False, description="Todo created_date"),
        'status':fields.String(required=True, descriptio='Todo Status', enum=["not_yet","started","completed","expired","unknown"]),
        'category_id':fields.Integer(required=True, description="Category Id"),
        
    }
)

@todo_name_space.route('/')
class Tdodo(Resource):
    @jwt_required(refresh=True)
    def get(self):
        return {"message":"Hello Tdoo"}
    def post(self):

        pass

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

