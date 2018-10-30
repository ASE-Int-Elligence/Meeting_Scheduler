from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from backend import app


# app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/meeting_scheduler.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))

    def __init__(self, email, password, username, firstname, lastname):
        self.email = email
        self.password = password
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return "%d/%s/%s" % (self.email, self.firstname, self.lastname)


if __name__ == "__main__":
    new_user = User(email="admin@gmail.com", password="admin", username="admin", firstname="Amy", lastname="Smith")
    db.session.add(new_user)
    db.cession.commit()

