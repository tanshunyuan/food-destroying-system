#!/usr/bin/env python
# -*- coding: utf-8 -*-
from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db

session = db.session


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    contactNumber = db.Column(db.Integer)
    password = db.Column(db.String)


class CustomerSchema(ModelSchema):
    class Meta:
        model = Customer


def create_customer(data):
    didSucceed = None
    new_customer = Customer(name=data['name'],
                            address=data['address'],
                            email=data['email'],
                            password=data['password'],
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
