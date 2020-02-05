#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from dotenv import load_dotenv
load_dotenv()


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """
    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning
