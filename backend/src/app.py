#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from loguru import logger
from dotenv import load_dotenv
from config import ConfigClass

from common.common import db
from common.seed import seed_food_itemsWcategory, seed_customer, seed_manager, seed_employee, seed_dispatcher
from model.customer import Customer, create_customer, get_customer, CustomerSchema
from model.manager import Manager, create_manager, get_manager, ManagerSchema
from model.employee import Employee, create_employee, get_employee, EmployeeSchema
from model.food import Food, get_all_food, get_food, create_food, update_food_category, FoodSchema
from model.category import Category, CategorySchema, create_category, get_category, get_all_category
from model.setmenu import SetMenu
load_dotenv()

# Create database
engine = create_engine(os.getenv('DB_URL'))
if not database_exists(engine.url):
    logger.info('Creating DB')
    create_database(engine.url)

app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

db.init_app(app)

# Create tables
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
    #clear_data(session)
    seed_food_itemsWcategory()
    seed_customer()
    seed_manager()
    seed_employee()


@app.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    result = create_customer(data)
    return jsonify(result, 200)


@app.route("/login", methods=['GET'])
def login():
    customer_schema = CustomerSchema()
    email = request.args.get('email')
    result = get_customer(email)
    if result is not None:
        return jsonify(customer_schema.dump(result), 200)
    else:
        return 'Customer not found', 404


@app.route("/api/manager/new", methods=['POST'])
def new_manager():
    data = request.get_json()
    result = create_manager(data)
    return jsonify(result, 200)


@app.route("/api/manager", methods=['GET'])
def manager_get():
    manager_schema = ManagerSchema()
    name = request.args.get('name')
    result = get_manager(name)
    if result is not None:
        return jsonify(manager_schema.dump(result), 200)
    else:
        return 'Manager not found', 404


@app.route("/api/employee/new", methods=['POST'])
def new_employee():
    data = request.get_json()
    result = create_employee(data)
    return jsonify(result, 200)


@app.route("/api/employee", methods=['GET'])
def employee_get():
    employee_schema = EmployeeSchema()
    name = request.args.get('name')
    result = get_employee(name)
    if result is not None:
        return jsonify(employee_schema.dump(result), 200)
    else:
        return 'Employee not found', 404


@app.route("/api/food/new", methods=['POST'])
def new_food():
    data = request.get_json()
    result = create_food(data)
    if result is not None:
        return jsonify(result, 200)
    else:
        return 'Something went wrong when creating ya food', 404


@app.route("/api/food/all", methods=['GET'])
def all_food():
    data = request.get_json()
    food_schemas = FoodSchema(many=True)
    result = get_all_food()
    return jsonify(food_schemas.dump(result), 200)


@app.route("/api/food", methods=['GET'])
def individual_food():
    data = request.get_json()
    food_schema = FoodSchema()
    id = request.args.get('id')
    result = get_food(id)
    logger.info(result)
    if result is not None:
        return jsonify(food_schema.dump(result), 200)
    else:
        return 'Employee not found', 404


@app.route("/api/food/category", methods=['PUT'])
def add_food_to_category():
    data = request.get_json()
    result = update_food_category(data)
    if result is not None:
        return jsonify(result, 200)
    else:
        return 'Something when wrong when adding your food to a category', 404


@app.route("/api/category/new", methods=['POST'])
def new_category():
    data = request.get_json()
    result = create_category(data)
    if result is not None:
        return jsonify(result, 200)
    else:
        return 'Something went wrong when creating ya category', 404


@app.route("/api/category/all", methods=['GET'])
def all_category():
    data = request.get_json()
    category_schemas = CategorySchema(many=True)
    result = get_all_category()
    return jsonify(category_schemas.dump(result), 200)


@app.route("/api/category", methods=['GET'])
def individual_category():
    data = request.get_json()
    category_schema = CategorySchema()
    id = request.args.get('id')
    result = get_category(id)
    logger.info(result)
    if result is not None:
        return jsonify(category_schema.dump(result), 200)
    else:
        return 'Category not found', 404
