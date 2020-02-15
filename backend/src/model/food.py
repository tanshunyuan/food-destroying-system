#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from common.common import db
from model.category import Category

session = db.session


class Food(db.Model):
    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = db.Column(db.String, unique=True)
    status = db.Column(db.Boolean)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    unit = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class FoodSchema(ModelSchema):
    class Meta:
        model = Food


def create_food(data):
    didSucceed = None
    logger.info(data)
    logger.info('lol')
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


def add_food_to_category(data):
    logger.info('Attempting to add food to a category')
    food_id = data['food_id']
    category_id = data['category_id']
    didSucceed = None

    query = session.query(Food).filter_by(id=food_id)
    food = query.first()
    result = query.update({Food.category_id: category_id})

    if result is not 0:
        session.commit()
        didSucceed = True
        logger.success('Successfully added setitem to a setmenu')
    else:
        session.rollback()
        logger.error('Failed to add setitem to a setmenu')
        didSucceed = False

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
        return e
        raise


def get_food(id):
    logger.info('Attempting to get food')
    try:
        result = session.query(Food).filter_by(id=id).first()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
