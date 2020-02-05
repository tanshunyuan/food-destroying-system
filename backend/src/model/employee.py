#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db

session = db.session


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    nric = db.Column(db.Integer)
    contactNumber = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    dateJoined = db.Column(db.DateTime)
    gender = db.Column(db.String)


class EmployeeSchema(ModelSchema):
    model = Employee


def create_employee(data):
    new_employee = Employee(name=data['name'],
                            nric=data['nric'],
                            contactNumber=data['contactNumber'],
                            dateJoined=data['dateJoined'],
                            status=data['status'],
                            gender=data['gender'])
    session.add(new_employee)
    logger.info('Attempting to create employee')
    try:
        session.commit()
        logger.success('Successfully created {} employee',
                       data['name'])
        didSucceed = True
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed
