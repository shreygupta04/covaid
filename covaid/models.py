from covaid import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(20), nullable=False) #
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(40), nullable=False)

    request = db.relationship('request', backref = 'author', lazy = True);
    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}')"

class request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ItemName = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    instruct = db.Column(db.String(500))
