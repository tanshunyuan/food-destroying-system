#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db, hashPassword
from .user import User

session = db.session


class Employee(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    nric = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    dateJoined = db.Column(db.DateTime)
    gender = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'employee',
    }


class EmployeeSchema(ModelSchema):
    class Meta:
        model = Employee


def create_employee(data):
    didSucceed = None
    passHash = hashPassword(data['password'])
    new_employee = Employee(name=data['name'],
                            email=data['email'],
                            nric=data['nric'],
                            contactNumber=data['contactNumber'],
                            dateJoined=data['dateJoined'],
                            status=data['status'],
                            passHash=passHash,
                            role='employee',
                            gender=data['gender'])
    session.add(new_employee)
    logger.info('Attempting to create employee')
    try:
        session.commit()
        logger.success('Successfully created {} employee', data['name'])
        didSucceed = new_employee.id
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


def get_employee(email):
    logger.info('Attempting to get employee')
    try:
        result = session.query(Employee).filter_by(email=email).first()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
