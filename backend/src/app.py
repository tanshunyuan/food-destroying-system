#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

from config import ConfigClass
from common.common import db
from common.seed import seed_food_items, seed_customer, seed_manager, seed_employee, seed_dispatcher
from model.customer import Customer, create_customer
from model.manager import Manager, create_manager
from model.employee import Employee, create_employee
from model.food import Food
from model.category import Category, add_food_item

app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')
db.init_app(app)

db.create_all(app=app)
session = db.session


def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()


@app.cli.command("seed")
def seed():
    print('SEED: Seeding DB...')
    clear_data(session)
    seed_food_items()
    seed_manager()
    seed_customer()
    seed_employee()
    seed_dispatcher()


@app.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    result = create_customer(data)
    return jsonify(result, 200)


@app.route("/api/manager/new", methods=['POST'])
def new_manager():
    data = request.get_json()
    result = create_manager(data)
    return jsonify(result, 200)


@app.route("/api/employee/new", methods=['POST'])
def new_employee():
    data = request.get_json()
    result = create_employee(data)
    return jsonify(result, 200)


@app.route("/api/item/new", methods=['POST'])
def addfooditem_under_category():
    data = request.get_json()
    result = add_food_item(data)
    return jsonify(result, 200)
