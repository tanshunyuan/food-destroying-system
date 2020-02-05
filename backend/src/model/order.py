#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger
import datetime

from common.common import db

session = db.session


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    createdDateTime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    deliveryDateTime = db.Column(db.DateTime)
    readyDateTime = db.Column(db.DateTime)
    orderedItems = db.Column(db.ARRAY(db.Integer))
    orderStatus = db.Column(db.String)
    totalAmount = db.Column(db.Integer)


class OrderSchema(ModelSchema):
    model = Order


def create_order(data):
    didSucceed = None
    new_order = Order(customer_id=data['customer_id'],
                      deliveryDateTime=data['deliveryDateTime'],
                      readyDateTime=data['readyDateTime'],
                      orderedItems=data['orderedItems'],
                      orderStatus=data['orderStatus'],
                      totalAmount=data['totalAmount'])

    session.add(new_order)
    logger.info('Attempting to create order')
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
