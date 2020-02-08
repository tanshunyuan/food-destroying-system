#!/usr/bin/env python
# -*- coding: utf-8 -*-
from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db, hashPassword
from .user import User

session = db.session


class Customer(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    address = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }


class CustomerSchema(ModelSchema):
    class Meta:
        model = Customer


def create_customer(data):
    didSucceed = None
    passHash = hashPassword(data['password'])
    new_customer = Customer(name=data['name'],
                            address=data['address'],
                            email=data['email'],
                            passHash=passHash,
                            role='customer',
                            contactNumber=data['contactNumber'])
    session.add(new_customer)
    logger.info('Attempting to create customer')
    try:
        session.commit()
        logger.success('Successfully created {} customer', data['name'])
        didSucceed = new_customer.id
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


def get_customer(email):
    logger.info('Attempting to get customer')
    try:
        result = session.query(Customer).filter_by(email=email).first()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
