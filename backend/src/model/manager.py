#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db, hashPassword
from .user import User

session = db.session


class Manager(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    nric = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    dateJoined = db.Column(db.DateTime)
    startDate = db.Column(db.DateTime)
    gender = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'manager',
    }


class ManagerSchema(ModelSchema):
    class Meta:
        model = Manager


def create_manager(data):
    didSucceed = None
    passHash = hashPassword(data['password'])
    new_manager = Manager(name=data['name'],
                          email=data['email'],
                          nric=data['nric'],
                          contactNumber=data['contactNumber'],
                          status=data['status'],
                          dateJoined=data['dateJoined'],
                          startDate=data['startDate'],
                          passHash=passHash,
                          role='manager',
                          gender=data['gender'])
    session.add(new_manager)
    logger.info('Attempting to create manager')
    try:
        session.commit()
        logger.success('Successfully created {} manager', data['name'])
        didSucceed = new_manager.id
    except Exception as e:
        print("Error ==> ", e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


def get_manager(email):
    logger.info('Attempting to get manager')
    try:
        result = session.query(Manager).filter_by(email=email).first()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
