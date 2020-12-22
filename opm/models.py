from datetime import datetime
from opm import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    profiles = db.relationship('Profiles', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}')"

class Profiles(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    profile_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.Text)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Profile('{self.profile_name}','{self.username}','{self.email}','{self.date_created}','{self.notes}')"
