from ..database import db
from datetime import datetime
from enum import Enum

class ToDoStatus(Enum):
    NOT_YET="not_yet"
    STARTED="started"
    COMPLETED="completed"
    EXPIRED="expired"
    UNKNOWN="unknown"



class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Integer(), nullable=False)
    description= db.Column(db.Text())
    completion_date=db.Column(db.DateTime())
    start_date=db.Column(db.DateTime(), default=datetime.utcnow)
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    status = db.Column(db.Enum(ToDoStatus), default=ToDoStatus.NOT_YET)
    category_id=db.Column(db.Integer(), db.ForeignKey('category.id'),nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'),nullable=False)

    def __str__(self) -> str:
        return f"Todo('{self.id}', '{self.name}')"
