#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db

session = db.session


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    nric = db.Column(db.Integer)
    contactNumber = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    dateJoined = db.Column(db.DateTime)
    gender = db.Column(db.String)
    password = db.Column(db.String)


class EmployeeSchema(ModelSchema):
    class Meta:
        model = Employee


def create_employee(data):
    didSucceed = None
    new_employee = Employee(name=data['name'],
                            email=data['email'],
                            nric=data['nric'],
                            contactNumber=data['contactNumber'],
                            dateJoined=data['dateJoined'],
                            status=data['status'],
                            password=data['password'],
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
