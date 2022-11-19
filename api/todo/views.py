from flask_restx import Resource,Namespace

todo_name_space = Namespace(name="todo", description='Todo Name space')

@todo_name_space.route('/')
class Tdodo(Resource):
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

