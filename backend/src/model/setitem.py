#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db
from model.food import Food

session = db.session

foodsetitem = db.Table(
    'foodsetitem',
    db.Column('setitem_id',
              db.Integer,
              db.ForeignKey('set_item.id'),
              primary_key=True),
    db.Column('food_id',
              UUID(as_uuid=True),
              db.ForeignKey('food.id'),
              primary_key=True))


class SetItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    setmenu_id = db.Column(db.Integer, db.ForeignKey('set_menu.id'))
    setmenufood = db.relationship('Food',
                                  secondary=foodsetitem,
                                  lazy='subquery',
                                  backref=db.backref('set_items', lazy=True))


def create_set_item(data):
    didSucceed = None
    new_set_item = SetItem(name=data['name'])
    session.add(new_set_item)
    logger.info('Attempting to create set item')

    try:
        session.commit()
        didSucceed = new_set_item.id
        logger.success('Successfully created {}', data['name'])
    except Exception as e:
        logger.info('Failed to create {}', data['name'])
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


def add_setitem_to_setmenu(data):
    logger.info('Attempting to add setitem to a setmenu')
    try:
        setitem_id = data['setitem_id']
        setmenu_id = data['setmenu_id']
        query = session.query(SetItem).filter_by(id=setitem_id)
        setitem = query.first()
        result = query.update({SetItem.setmenu_id: setmenu_id})
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise


def add_food_to_setitem(data):
    didSucceed = None
    logger.info('Attempting to update set item into a set menu')
    setitem_id = data['setitem_id']
    food_ids = data['food_ids']
    logger.info('food ids {}', food_ids)

    food_array = [
        session.query(Food).filter_by(id=food_id).first()
        for food_id in food_ids
    ]

    setitem = session.query(SetItem).filter_by(id=setitem_id).first()

    if setitem is not None:
        setitem.setmenufood = food_array

    try:
        session.commit()
        for food in food_array:
            logger.success('Successfully added {} to set item {}', food.name,
                           setitem_id)
    except Exception as e:
        logger.info('Failed to add food to setitem')
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed
