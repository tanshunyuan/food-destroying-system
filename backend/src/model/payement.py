#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger
import datetime

from common.common import db

session = db.session


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiptNumber = db.Column(db.Integer)
    paymentDateTime = db.Column(db.DateTime)
    paymentItems = db.Column(db.ARRAY(db.Integer)) 
    paymentType = db.Column(db.String)
    paymentAmount = db.Column(db.Integer)


class PaymentSchema(ModelSchema):
    model = Payment


def create_payment(data):
    didSucceed = None
    new_payment = Payment(
        receiptNumber=data['receiptNumber'],
        paymentDateTime=data['paymentDateTime'],
        paymentItems=data['paymentItems'],
        paymentType=data['paymentType'],
        paymentAmount=data['paymentAmount']
    )

    session.add(new_payment)
    logger.info('Attempting to create payment')
    try:
        session.commit()
        logger.info('Successfully created order number {}', data['id'])
        didSucceed = True
    except Exception as e:
        logger.info('Failed to create order')
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed
