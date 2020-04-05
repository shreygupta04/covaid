from covaid import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    requests = db.relationship('Request', backref = 'request', lazy = True)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}')"

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column((db.String(50)), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    instruct = db.Column(db.String(500))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
