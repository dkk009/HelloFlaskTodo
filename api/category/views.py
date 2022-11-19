from flask_restx import Resource, Namespace

category_name_space = Namespace(name='category', description="Category name space")

@category_name_space.route("/")
class Category(Resource):
    def post(self):
        pass
    def get(self):
        pass

@category_name_space.route("/<int:category_id>")
class GetOrUpdateCategory(Resource):
    def get(self, category_id):
        pass
    def put(self, category_id):
        pass
    def delete(self, category_id):
        pass
