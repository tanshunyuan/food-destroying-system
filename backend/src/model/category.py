#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema, TableSchema
from loguru import logger

from common.common import db

session = db.session


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    food = db.relationship('Food', backref='category', lazy=True)


class CategorySchema(TableSchema):
    class Meta:
        table = Category.__table__


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

def get_all_category():
    logger.info('Attempting to get all category')
    try:
        result = session.query(Category).all()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise


def get_category(id):
    logger.info('Attempting to get category')
    try:
        result = session.query(Category).filter_by(id=id).first()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
