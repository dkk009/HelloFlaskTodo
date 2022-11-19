from attr import dataclass
from ..database import db

class User(db.Model):
    _table_name__= 'user'
    id = db.Column(db.Integer(),primary_key=True)
    user_name = db.Column(db.String(64),nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password=db.Column(db.Text(), nullable=False)
    name = db.Column(db.String(128),nullable=False, unique=False)
    todos = db.relationship('Todo', backref='user', lazy=True)
    categories = db.relationship('Category', backref='user', lazy=True)
    def __repr__(self):
        return f"User('{self.user_name}')"

    def __init__(self,email,password,name ):
        self.user_name = email
        self.email = email
        self.password = password
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def as_dict(self):
        return {c.name:getattr(self,c.name) for c in self.__table__.columns}