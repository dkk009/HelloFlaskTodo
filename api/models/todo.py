from ..database import db
from datetime import datetime
from enum import Enum

class ToDoStatus(Enum):
    CREATED="CREATED"
    STARTED="STARTED"
    COMPLETED="COMPLETED"
    EXPIRED="EXPIRED"
    UNKNOWN="UNKNOWN"



class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Integer(), nullable=False)
    description= db.Column(db.Text())
    completion_date=db.Column(db.DateTime(),default=datetime.utcnow)
    start_date=db.Column(db.DateTime(), default=datetime.utcnow)
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    status = db.Column(db.Enum(ToDoStatus), default=ToDoStatus.CREATED)
    category_id=db.Column(db.Integer(), db.ForeignKey('category.id'),nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, description, start_date, status,category_id,user_id):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.status = status
        self.category_id = category_id
        self.user_id = user_id
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    def __str__(self) -> str:
        return f"Todo('{self.id}', '{self.name}')"
