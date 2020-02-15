#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.dialects.postgresql import UUID
from loguru import logger
import datetime

from common.common import db
from model.food import Food, FoodSchema

session = db.session

orderfood = db.Table(
    'orderfood',
    db.Column('order_id',
              db.Integer,
              db.ForeignKey('order.id'),
              primary_key=True),
    db.Column('food_id',
              UUID(as_uuid=True),
              db.ForeignKey('food.id'),
              primary_key=True))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    orderedItems = db.relationship('Food',
                                   secondary=orderfood,
                                   lazy='subquery',
                                   backref=db.backref('order', lazy=True))
    createdDateTime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    deliveryDateTime = db.Column(db.DateTime)
    readyDateTime = db.Column(db.DateTime)
    orderStatus = db.Column(db.String)
    totalAmount = db.Column(db.Integer)


class OrderSchema(ModelSchema):
    orderedItems = Nested(FoodSchema, many=True)

    class Meta:
        model = Order
        include_fk = True


def create_order(data):
    didSucceed = None
    new_order = Order(customer_id=data['customer_id'],
                      deliveryDateTime=data['deliveryDateTime'],
                      readyDateTime=data['readyDateTime'],
                      orderStatus=data['orderStatus'],
                      totalAmount=data['totalAmount'])
    food_ids = data['food_ids']
    food_array = [
        session.query(Food).filter_by(id=food_id).first()
        for food_id in food_ids
    ]
    new_order.orderedItems = food_array

    session.add(new_order)
    logger.info('Attempting to create order')
    try:
        session.commit()
        logger.info('Successfully created order number {}', new_order.id)
        didSucceed = new_order.id
    except Exception as e:
        logger.info('Failed to create order')
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


def get_all_order():
    logger.info('Attempting to get all order')
    try:
        result = session.query(Order).all()
        logger.info(result)
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise


def get_order(id):
    logger.info('Attempting to get order')
    try:
        result = session.query(Order).filter_by(id=id).first()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise


def get_order_by_customer_id(id):
    logger.info('Attempting to get order')
    try:
        result = session.query(Order).filter_by(customer_id=id).first()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
