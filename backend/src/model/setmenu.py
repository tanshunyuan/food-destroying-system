#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db
from model.food import Food

session = db.session

setmenufood = db.Table(
    'setmenufood',
    db.Column('setmenu_id',
              db.Integer,
              db.ForeignKey('set_menu.id'),
              primary_key=True),
    db.Column('food_id',
              UUID(as_uuid=True),
              db.ForeignKey('food.id'),
              primary_key=True))


class SetMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    totalPrice = db.Column(db.Integer)
    size = db.Column(db.Integer)
    setmenufood = db.relationship('Food',
                                  secondary=setmenufood,
                                  lazy='subquery',
                                  backref=db.backref('set_menus', lazy=True))


class SetMenuSchema(ModelSchema):
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


def update_food_set_menu(data):
    didSucceed = None
    logger.info('Attempting to update food set menu')
    food_ids = data['id']
    setmenu_id = data['setmenu_id']
    logger.info('food_id {} and setmenu_id {}', food_ids, setmenu_id)

    food_id_array = [
        session.query(Food).filter_by(id=food_id).first()
        for food_id in food_ids
    ]
    setmenu = session.query(SetMenu).filter_by(id=setmenu_id).first()
    setmenu.setmenufood = food_id_array

    try:
        session.commit()
        logger.success('Successfully created {}', data['name'])
    except Exception as e:
        logger.info('Failed to create {}', data['name'])
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed
