#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """
    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@localhost:5432/fooddestroyingsystem'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@se_postgresdb/fooddestroyingsystem'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning
