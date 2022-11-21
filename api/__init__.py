from flask import Flask
from flask_restx import Api
from .auth.views import auth_name_space
from .todo.views import todo_name_space
from .category.views import category_name_space
from .config.config import config_dict
from .database import db
from .models.todo import Todo
from .models.category import Category
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

def create_app(config = config_dict['prod']):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate = Migrate(app=app,db=db)
    api = Api(app=app)
    api.add_namespace(auth_name_space, path="/auth")
    api.add_namespace(todo_name_space, path='/todo')
    api.add_namespace(category_name_space, path='/category')
    jwt = JWTManager(app)
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'user': User,
            'category':Category,
            'todo':Todo
        }

    return app