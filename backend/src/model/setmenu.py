#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db

session = db.session


class SetMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    totalPrice = db.Column(db.Integer)
    size = db.Column(db.Integer)


class SetMenuSchema(ModelSchema):
    class Meta:
        model = SetMenu


def create_set_menu(data):
    didSucceed = None
    new_set_menu = SetMenu(name=data['name'],
                           totalPrice=data['totalPrice'],
                           size=data['size'])
    session.add(new_set_menu)
    logger.info('Attempting to create set menu')

    try:
        session.commit()
        didSucceed = new_set_menu.id
        logger.success('Successfully created {}', data['name'])
    except Exception as e:
        logger.info('Failed to create {}', data['name'])
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


def get_all_setmenu():
    logger.info('Attempting to get all setmenu')
    try:
        result = session.query(SetMenu).all()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise


def get_setmenu(id):
    logger.info('Attempting to get setmenu')
    try:
        result = session.query(SetMenu).filter_by(id=id).first()
        return result
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
