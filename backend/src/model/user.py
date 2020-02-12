import os
import bcrypt
from loguru import logger
from marshmallow_sqlalchemy import ModelSchema
from flask import jsonify

from common.common import db

session = db.session


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    passHash = db.Column(db.String)
    contactNumber = db.Column(db.String)
    role = db.Column(db.String)
    __mapper_args__ = {'polymorphic_identity': 'user', 'polymorphic_on': role}


class UserSchema(ModelSchema):
    class Meta:
        model = User


user_schema = UserSchema()
user_schemas = UserSchema(many=True)


def get_user(email):
    try:
        user = session.query(User).filter_by(email=email).first()
        return user
    except Exception as e:
        print(e)


def comparePassword(password, passHash):
    password = password.encode('utf-8')
    passHash = passHash.encode('utf-8')
    return bcrypt.checkpw(password, passHash)


def authenticate_user(email, password):
    user_data = get_user(email)
    if user_data is None:
        return "User is not found", 401
    user = user_schema.dump(user_data)
    is_password_correct = comparePassword(password, user['passHash'])
    if is_password_correct:
        logger.info('password_correct')
        # Remove sensitive fields before response
        del user['passHash']
        del user['email']
        # Convert id from int to string
        user['id'] = str(user['id'])
        return jsonify(user=user), 200
    else:
        logger.error('password wrong')
        return 'Email and password combination is incorrect', 401
