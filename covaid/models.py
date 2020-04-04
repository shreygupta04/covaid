from covaid import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(40), nullable=False)

    # orders = db.Column(db.ARRAY())
    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}')"
