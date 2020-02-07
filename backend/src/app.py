#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

from config import ConfigClass
from common.common import db
from common.seed import seed_food_itemsWcategory, seed_customer, seed_manager, seed_employee, seed_dispatcher
from model.customer import Customer, create_customer
from model.manager import Manager, create_manager
from model.employee import Employee, create_employee
from model.food import Food, get_all_food, FoodSchema
from model.category import Category
from model.setmenu import SetMenu

app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

db.init_app(app)
db.create_all(app=app)


def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()


@app.cli.command("seed")
def seed():
    session = db.session
    print('SEED: Seeding DB...')
    clear_data(session)
    seed_food_itemsWcategory()


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


@app.route("/api/food/all", methods=['GET'])
def all_food():
    data = request.get_json()
    food_schemas = FoodSchema(many=True)
    result = get_all_food()
    logger.info(result)
    return jsonify(food_schemas.dump(result), 200)
