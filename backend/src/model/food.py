#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db

session = db.session


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    status = db.Column(db.Boolean)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    unit = db.Column(db.Integer)


class FoodSchema(ModelSchema):
    model = Food


def create_food(data):
    didSucceed = None
    new_food = Food(name=data['name'],
                    status=data['status'],
                    price=data['price'],
                    description=data['description'],
                    unit=data['unit'])
    session.add(new_food)
    logger.info('Attempting to create food')
    try:
        session.commit()
        logger.success('Successfully created {}', data['name'])
        didSucceed = new_food.id
    except Exception as e:
        logger.info('Failed to create {}', data['name'])
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


def get_all_food():
    logger.info('Attempting to get all food')
    try:
        result = session.query(Food).all()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise


def get_food(data):
    logger.info('Attempting to get food')
    try:
        result = session.query(Food).filter_by(data['id']).first()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
