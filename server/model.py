from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from dataclasses import dataclass

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    devices = db.relationship('Device')

@dataclass
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.relationship('Data')

@dataclass
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.Integer)
    datetime =db.Column(db.DateTime(timezone=True), default=func.now())
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'datum': self.datum,
            'datetime': self.datetime,
            'device_id': self.device_id
        }

class CurrentUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_user = db.Column(db.Integer)
