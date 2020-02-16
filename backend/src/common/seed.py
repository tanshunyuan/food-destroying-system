#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.food import create_food, add_food_to_category
from model.category import create_category
from model.setmenu import create_set_menu
from model.setitem import create_set_item, add_food_to_setitem, add_setitem_to_setmenu
from model.order import create_order
from model.customer import create_customer
from model.manager import create_manager
from model.dispatcher import create_dispatcher
from model.employee import create_employee
from loguru import logger


def mainseed():
    category_ids = seed_category()
    food_ids = seed_food_items()
    set_menu_ids = seed_set_menu()
    set_item_ids = seed_set_item()
    customer_id = seed_customer()
    manager_id = seed_manager()
    employee_id = seed_employee()
    dispatcher_id = seed_dispatcher()
    order_id = seed_order(customer_id, food_ids)

    x = 0
    for category_id in category_ids:
        add_food_to_category({
            'food_id': food_ids[x],
            'category_id': category_id
        })
        x = x + 1

    y = 0
    for set_menu_id in set_menu_ids:
        add_setitem_to_setmenu({
            'setitem_id': set_item_ids[y],
            'setmenu_id': set_menu_id
        })
        y = y + 1

    for set_item_id in set_item_ids:
        add_food_to_setitem({'food_ids': food_ids, 'setitem_id': set_item_id})


def seed_order(customer_id, food_ids):
    data = {
        'customer_id': customer_id,
        'deliveryDateTime': '2020-01-20 12:18:23 UTC',
        'readyDateTime': '2020-01-21 12:18:23 UTC',
        'orderStatus': 'new',
        'totalAmount': 100,
        'food_ids': food_ids
    }

    order_id = create_order(data)
    return order_id


def seed_food_items():
    data = [
        {
            'name': 'Chicken Burger',
            'status': True,
            'price': 10,
            'description': 'This is a chicken burger',
            'unit': 100,
        },
        {
            'name': 'Fish Burger',
            'status': True,
            'price': 10,
            'description': 'This is a fish burger',
            'unit': 100,
        },
        {
            'name': 'Tiramisu',
            'status': True,
            'price': 10,
            'description': 'This is a tiramisu',
            'unit': 100,
        },
        {
            'name': 'Pepsi',
            'status': True,
            'price': 10,
            'description': 'This is a pepsi',
            'unit': 100,
        },
    ]
    food_ids = []
    for row in data:
        food_id = create_food(row)
        food_ids.append(food_id)
    return food_ids


def seed_category():
    data = ['Chicken', 'Fish', 'Desert', 'Beverages']
    category_ids = []
    for name in data:
        category_id = create_category({'name': name})
        category_ids.append(category_id)
    return category_ids


def seed_set_menu():
    data = ['Breakfast', 'Lunch', 'Dinner']
    set_menu_ids = []
    for name in data:
        set_menu_id = create_set_menu({'name': name})
        set_menu_ids.append(set_menu_id)

    return set_menu_ids


def seed_set_item():
    data = [
        {
            'name': 'Platter One',
            'totalPrice': 100,
            'size': 10
        },
        {
            'name': 'Platter Two',
            'totalPrice': 100,
            'size': 10
        },
        {
            'name': 'Platter Three',
            'totalPrice': 100,
            'size': 10
        },
    ]
    set_item_ids = []
    for row in data:
        set_item_id = create_set_item(row)
        set_item_ids.append(set_item_id)

    return set_item_ids


def seed_customer():
    data = {
        'name': 'customer',
        'address': 'Washinton state',
        'email': 'customer@gmail.com',
        'contactNumber': 123456,
        'password': 'password'
    }
    return create_customer(data)


def seed_manager():
    data = {
        'name': 'manager',
        'email': 'manager@gmail.com',
        'nric': 8888888,
        'contactNumber': 123456,
        'dateJoined': '2020-01-20 12:18:23 UTC',
        'startDate': '2020-01-22 12:18:23 UTC',
        'status': True,
        'gender': 'Male',
        'password': 'password',
    }
    create_manager(data)


def seed_employee():
    data = {
        'name': 'employee',
        'email': 'employee@gmail.com',
        'nric': 9999999,
        'contactNumber': 123456,
        'dateJoined': '2020-01-20 12:18:23 UTC',
        'status': True,
        'gender': 'Male',
        'password': 'password'
    }
    return create_employee(data)


def seed_dispatcher():
    data = {
        'name': 'genos',
        'commission': 100.33,
        'email': 'dispatcher@gmail.com'
    }
    return create_dispatcher(data)
