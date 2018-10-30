from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from __init__ import app


# app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/meeting_scheduler.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))

    def __init__(self, email, password, username, firstname, lastname, active=True):
        self.email = email
        self.password = password
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.active = active

    def __repr__(self):
        return "%d/%s/%s" % (self.email, self.firstname, self.lastname)
    
    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


if __name__ == "__main__":
    db.create_all()
    new_user = User(email="admin@gmail.com", password="admin", username="admin", firstname="Amy", lastname="Smith")
    db.session.add(new_user)
    db.session.commit()

