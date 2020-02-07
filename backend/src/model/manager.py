#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db

session = db.session


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    nric = db.Column(db.Integer)
    contactNumber = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    dateJoined = db.Column(db.DateTime)
    startDate = db.Column(db.DateTime)
    gender = db.Column(db.String)
    password = db.Column(db.String)


class ManagerSchema(ModelSchema):
    class Meta:
        model = Manager


def create_manager(data):
    didSucceed = None
    new_manager = Manager(name=data['name'],
                          nric=data['nric'],
                          contactNumber=data['contactNumber'],
                          status=data['status'],
                          dateJoined=data['dateJoined'],
                          startDate=data['startDate'],
                          password=data['password'],
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


def get_manager(name):
    logger.info('Attempting to get manager')
    try:
        result = session.query(Manager).filter_by(name=name).first()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
