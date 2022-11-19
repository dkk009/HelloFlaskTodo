from ..database import db
from datetime import datetime

class Category(db.Model):
    __table_name__='category'
    id= db.Column(db.Integer(), primary_key=True)
    name= db.Column(db.String(128), nullable=False)
    user_id =db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    created_date=db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    def __str__(self) -> str:
        return f"Category('{self.id},{self.name},{self.user_id})"
        