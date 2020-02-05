#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import db

session = db.session


class Dispatcher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    commission = db.Column(db.Float)


class DispatcherSchema(ModelSchema):
    model = Dispatcher


def create_dispatcher(data):
    didSucceed = None
    new_dispatcher = Dispatcher(
        name=data['name'],
        commission=data['commission'],
    )
    session.add(new_dispatcher)
    logger.info('Attempting to create dispatcher')
    try:
        session.commit()
        logger.success('Successfully created {}', data['name'])
        didSucceed = new_dispatcher.id
    except Exception as e:
        logger.info('Failed to create {}', data['name'])
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed
