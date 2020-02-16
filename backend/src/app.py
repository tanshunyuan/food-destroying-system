#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from loguru import logger
from config import ConfigClass
from sqlalchemy.dialects.postgresql import UUID
from flask_cors import CORS

from common.common import db
from common.seed import mainseed
from model.user import authenticate_user
from model.food import Food, FoodSchema, get_all_food, get_food, create_food, add_food_to_category, update_food, delete_food
from model.category import Category, CategorySchema, create_category, get_category, get_all_category
from model.setmenu import SetMenu, SetMenuSchema, create_set_menu, get_all_setmenu
from model.setitem import SetItem, SetItemSchema, create_set_item, add_food_to_setitem, get_all_setitem, add_setitem_to_setmenu
from model.order import Order, OrderSchema, create_order, get_order, get_order_by_customer_id, get_all_order, update_order_status

#Create database
engine = create_engine(
    'postgresql://postgres:mysecretpassword@localhost:5432/fooddestroyingsystem'
    #'postgresql://postgres:mysecretpassword@se_postgresdb/fooddestroyingsystem'
)

if not database_exists(engine.url):
    logger.info('Creating DB')
    create_database(engine.url)

app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

db.init_app(app)

CORS(app)
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
    mainseed()


@app.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    result = create_customer(data)
    return jsonify(result), 200


@app.route("/login", methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    return authenticate_user(email, password)


@app.route("/api/manager", methods=['POST'])
def new_manager():
    data = request.get_json()
    result = create_manager(data)
    return jsonify(result), 200


@app.route("/api/manager", methods=['GET'])
def retrieve_manager():
    manager_schema = ManagerSchema()
    email = request.args.get('email')
    result = get_manager(email)
    if result is not None:
        return jsonify(manager_schema.dump(result)), 200
    else:
        return 'Manager not found', 404


@app.route("/api/employee", methods=['POST'])
def new_employee():
    data = request.get_json()
    result = create_employee(data)
    return jsonify(result), 200


@app.route("/api/employee", methods=['GET'])
def retrieve_employee():
    employee_schema = EmployeeSchema()
    email = request.args.get('email')
    result = get_employee(email)
    if result is not None:
        return jsonify(employee_schema.dump(result)), 200
    else:
        return 'Employee not found', 404


@app.route("/api/food", methods=['POST'])
def new_food():
    data = request.get_json()
    result = create_food(data)
    if result is not None:
        return jsonify(food_id=result), 200
    else:
        return 'Something went wrong when creating food', 404


@app.route("/api/food", methods=['PUT'])
def update_a_food():
    data = request.get_json()
    result = update_food(data)
    if result is not None:
        return jsonify(result), 200
    else:
        return 'Something went wrong when updating food', 404


@app.route("/api/food", methods=['DELETE'])
def delete_a_food():
    data = request.get_json()
    result = delete_food(data)
    if result is not None:
        return jsonify(result), 200
    else:
        return 'Something went wrong when deleting food', 404


@app.route("/api/food/all", methods=['GET'])
def retrieve_foods():
    data = request.get_json()
    food_schemas = FoodSchema(many=True)
    result = get_all_food()
    return jsonify(result=food_schemas.dump(result)), 200


@app.route("/api/food", methods=['GET'])
def retrieve_food():
    food_schema = FoodSchema()
    id = request.args.get('id', default='', type=str)
    if id == "":
        return 'Food not found', 404

    result = get_food(id)
    logger.info(result)
    if result is not None:
        return jsonify(food_schema.dump(result)), 200
    else:
        return 'Food not found', 404


@app.route("/api/food/category", methods=['POST'])
def assign_food_to_category():
    data = request.get_json()
    result = add_food_to_category(data)
    if result is not None:
        return jsonify(result), 200
    else:
        return 'Something when wrong when adding your food to a category', 404


@app.route("/api/category", methods=['POST'])
def new_category():
    data = request.get_json()
    result = create_category(data)
    if result is not None:
        return jsonify(result), 200
    else:
        return 'Something went wrong when creating category', 404


@app.route("/api/category/all", methods=['GET'])
def retrieve_categories():
    data = request.get_json()
    category_schemas = CategorySchema(many=True)
    result = get_all_category()
    return jsonify(result=category_schemas.dump(result)), 200


@app.route("/api/category", methods=['GET'])
def retrieve_category():
    data = request.get_json()
    category_schema = CategorySchema()
    id = request.args.get('id')
    result = get_category(id)
    logger.info(result)
    if result is not None:
        return jsonify(category_schema.dump(result)), 200
    else:
        return 'Category not found', 404


@app.route("/api/food/setitem", methods=['POST'])
def assign_food_to_setitem():
    data = request.get_json()
    result = add_food_to_setitem(data)
    if result is not None:
        return jsonify(result), 200
    else:
        return 'Something when wrong when adding your food to a setitem', 404


@app.route("/api/setitem/setmenu", methods=['POST'])
def assign_setitem_to_setmenu():
    data = request.get_json()
    result = add_setitem_to_setmenu(data)
    if result is True:
        return jsonify(result), 200
    else:
        return jsonify('Something when wrong when adding setitem to a setmenu',
                       404)


@app.route("/api/setmenu", methods=['POST'])
def new_setmenu():
    data = request.get_json()
    result = create_set_menu(data)
    if result is not None:
        return jsonify(setmenu_id=result), 200
    else:
        return 'Something went wrong when creating setmenu', 404


@app.route("/api/setmenu/all", methods=['GET'])
def retrieve_setmenus():
    data = request.get_json()
    setmenu_schemas = SetMenuSchema(many=True)
    result = get_all_setmenu()
    return jsonify(result=setmenu_schemas.dump(result)), 200


@app.route("/api/setmenu", methods=['GET'])
def retrieve_setmenu():
    data = request.get_json()
    setmenu_schema = SetMenuSchema()
    id = request.args.get('id')
    result = get_setmenu(id)
    logger.info(result)
    if result is not None:
        return jsonify(setmenu_schema.dump(result)), 200
    else:
        return 'Set Menu not found', 404


@app.route("/api/setitem", methods=['POST'])
def new_set_item():
    data = request.get_json()
    result = create_set_item(data)
    if result is not None:
        print(result)
        return jsonify(setitem_id=result), 200
    else:
        return 'Something went wrong when creating setitem', 404


@app.route("/api/setitem/all", methods=['GET'])
def retrieve_setitems():
    setitem_schemas = SetItemSchema(many=True)
    result = get_all_setitem()
    return jsonify(setitem_schemas.dump(result)), 200


@app.route("/api/setitem", methods=['GET'])
def retrieve_setitem():
    setitem_schema = SetItemSchema()
    id = request.args.get('id')
    result = get_setitem(id)
    logger.info(result)
    if result is not None:
        return jsonify(setitem_schema.dump(result)), 200
    else:
        return 'Set Item not found', 404


@app.route("/api/order", methods=['POST'])
def new_order():
    data = request.get_json()
    result = create_order(data)
    if result is not None:
        print(result)
        return jsonify(order_id=result), 200
    else:
        return 'Something went wrong when creating order', 404


@app.route("/api/order/all", methods=['GET'])
def retrieve_orders():
    order_schemas = OrderSchema(many=True)
    result = get_all_order()
    return jsonify(order_schemas.dump(result)), 200


@app.route("/api/order/customer", methods=['GET'])
def retrieve_order_by_customer():
    customer_id = request.args.get('customer_id')
    order_schema = OrderSchema()
    result = get_order_by_customer_id(customer_id)
    return jsonify(setitem_schemas.dump(result)), 200


@app.route("/api/order", methods=['PUT'])
def update_order_statuses():
    data = request.get_json()
    result = update_order_status(data)
    if result is not None:
        return jsonify(result), 200
    else:
        return 'Something went wrong when updating order', 404
