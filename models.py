from app import db

class Messages(db.Model):
    __tablename__ = "messages"
    id = db.Column('id', db.Integer, primary_key=True)
    message = db.Column('message', db.Unicode)