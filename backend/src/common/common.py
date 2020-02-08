#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()


def hashPassword(password):
    encodedpassword = password.encode('utf-8')
    return bcrypt.hashpw(encodedpassword, bcrypt.gensalt()).decode('utf-8')
