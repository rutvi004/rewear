from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    points = db.Column(db.Integer, default=100)
    is_admin = db.Column(db.Boolean, default=False)

class ClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    size = db.Column(db.String(20))
    condition = db.Column(db.String(20))
    tags = db.Column(db.String(100))
    image = db.Column(db.String(100))
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='available')  # available, swapped
