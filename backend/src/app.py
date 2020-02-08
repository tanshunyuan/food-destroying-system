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
from model.customer import Customer, CustomerSchema, create_customer, get_customer
from model.manager import Manager, ManagerSchema, create_manager, get_manager
from model.employee import Employee, EmployeeSchema, create_employee, get_employee
from model.food import Food, FoodSchema, get_all_food, get_food, create_food, add_food_to_category
from model.category import Category, CategorySchema, create_category, get_category, get_all_category
from model.setmenu import SetMenu, SetMenuSchema, create_set_menu, get_all_setmenu
from model.setitem import SetItem, SetItemSchema, create_set_item, add_food_to_setitem, get_all_setitem, add_setitem_to_setmenu
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
    clear_data(session)
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
    email = request.args.get('email')
    result = get_manager(email)
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
    email = request.args.get('email')
    result = get_employee(email)
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


@app.route("/api/food/category", methods=['POST'])
def addFoodToCategory():
    data = request.get_json()
    result = add_food_to_category(data)
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


@app.route("/api/food/setitem", methods=['POST'])
def addFoodToSetItem():
    data = request.get_json()
    result = add_food_to_setitem(data)
    if result is not None:
        return jsonify(result, 200)
    else:
        return 'Something when wrong when adding your food to a setitem', 404


@app.route("/api/setitem/setmenu", methods=['POST'])
def addSetItemToSetMenu():
    data = request.get_json()
    result = add_setitem_to_setmenu(data)
    if result is True:
        return jsonify(result, 200)
    else:
        return jsonify('Something when wrong when adding setitem to a setmenu',
                       404)


@app.route("/api/setmenu/new", methods=['POST'])
def new_setmenu():
    data = request.get_json()
    result = create_set_menu(data)
    if result is not None:
        return jsonify(result, 200)
    else:
        return 'Something went wrong when creating setmenu', 404


@app.route("/api/setmenu/all", methods=['GET'])
def all_setmenu():
    data = request.get_json()
    setmenu_schemas = SetMenuSchema(many=True)
    result = get_all_setmenu()
    return jsonify(setmenu_schemas.dump(result), 200)


@app.route("/api/setmenu", methods=['GET'])
def retrieve_one_setmenu():
    data = request.get_json()
    setmenu_schema = SetMenuSchema()
    id = request.args.get('id')
    result = get_setmenu(id)
    logger.info(result)
    if result is not None:
        return jsonify(setmenu_schema.dump(result), 200)
    else:
        return 'Set Menu not found', 404


@app.route("/api/setitem/new", methods=['POST'])
def new_set_item():
    data = request.get_json()
    result = create_set_item(data)
    if result is not None:
        return jsonify(result, 200)
    else:
        return 'Something went wrong when creating setitem', 404


@app.route("/api/setitem/all", methods=['GET'])
def all_setitem():
    data = request.get_json()
    setitem_schemas = SetItemSchema(many=True)
    result = get_all_setitem()
    return jsonify(setitem_schemas.dump(result), 200)


@app.route("/api/setitem", methods=['GET'])
def retrieve_one_setitem():
    data = request.get_json()
    setitem_schema = SetItemSchema()
    id = request.args.get('id')
    result = get_setitem(id)
    logger.info(result)
    if result is not None:
        return jsonify(setitem_schema.dump(result), 200)
    else:
        return 'Set Item not found', 404
