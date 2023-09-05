from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)

    def __init__(self, userId, title, body):
        self.userId = userId
        self.title = title
        self.body = body

    def to_dict(self):
        return {
            "userId": self.userId,
            "id": self.id,
            "title": self.title,
            "body": self.body
        }
