#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db

session = db.session


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    foods = db.relationship('Food', backref='category', lazy=True)


class CategorySchema(ModelSchema):
    model = Category


def create_category(data):
    didSucceed = None
    new_category = Category(name=data['name'])
    logger.info('Attempting to create category')
    session.add(new_category)
    try:
        session.commit()
        didSucceed = new_category.id
        logger.success('Successfully created {} category', data['name'])
    except Exception as e:
        logger.info('Failed to create {} category', data['name'])
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


#def add_food_item(data):
#    didSucceed = None
#    category_id = data['id']
#    category = session.query(Category).filter_by(id=category_id).first()
#
#    for item in data['foodItems']:
#        category.foodItems.append(item)
#
#    session.query(Category).filter_by(id=category_id).\
#        update({'foodItems':category.foodItems}, synchronize_session='evaluate')
#    logger.info('Attempting to add food items')
#    try:
#        session.commit()
#        didSucceed = True
#    except Exception as e:
#        logger.error(e)
#        session.rollback()
#        raise
#    finally:
#        session.close()
#        return didSucceed


def get_all_category():
    logger.info('Attempting to get all category')
    try:
        result = session.query(Category).all()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise


def get_category(data):
    logger.info('Attempting to get category')
    try:
        result = session.query(Category).filter_by(data['id']).first()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
