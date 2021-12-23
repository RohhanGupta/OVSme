from enum import unique
from flask import url_for
from sqlalchemy.orm import defaultload
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class voter(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    img = db.Column(db.Text, unique=True, default=None)
    phone_number = db.Column(db.Integer(), unique=True)
    password_1 = db.Column(db.String(120))
    password_2 = db.Column(db.String(120))
    voted = db.Column(db.Integer(), nullable=False, default=0)
    admin = db.Column(db.String(10), default="Not Admin")
    status = db.Column(db.String(10), default="Not Verified")
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class candidate(db.Model, UserMixin):
    id = db.Column(db.Integer,nullable=False, primary_key=True)
    candidate_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(50),nullable=False, unique=True)
    vote_count = db.Column(db.Integer(), nullable=False, default=0)
    date_created = db.Column(db.DateTime(timezone=True),nullable=False, default=func.now())