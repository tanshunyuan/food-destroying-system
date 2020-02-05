#!/usr/bin/env python
# -*- coding: utf-8 -*-


from marshmallow_sqlalchemy import ModelSchema
from loguru import logger
import datetime

from common.common import db

session = db.session


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    deliveryDateTime = db.Column(db.DateTime)
    orderedItems = db.Column(db.ARRAY(db.Integer))
    orderSummary = db.Column(db.Integer)


class Receipt(ModelSchema):
    model = Order


def create_receipt(data):
    didSucceed = None
    new_receipt = Receipt(order_id=data['customer_id'],
                        payment_id=data['payment_id'],
                      deliveryDateTime=data['deliveryDateTime'],
                      orderedItems=data['orderedItems'],
                      orderSummary=data['orderSummary'])

    session.add(new_receipt)
    logger.info('Attempting to create receipt')
    try:
        session.commit()
        logger.info('Successfully created order number {}', data['id'])
        didSucceed = new_order.id
    except Exception as e:
        logger.info('Failed to create order')
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed
