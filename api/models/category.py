from ..database import db
from datetime import datetime

class Category(db.Model):
    __table_name__='category'
    id= db.Column(db.Integer(), primary_key=True)
    name= db.Column(db.String(128), nullable=False)
    description= db.Column(db.Text(), nullable=True)
    user_id =db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    created_date=db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def __str__(self) -> str:
        return f"Category('{self.id},{self.name},{self.user_id})"
    
    def __init__(self, name,description,user_id) -> None:
        self.name = name
        self.description = description
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def as_dict(self):
        return {c.name:getattr(self,c.name) for c in self.__table__.columns}
        