#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.food import create_food, add_food_to_category
from model.category import create_category
from model.setmenu import create_set_menu
from model.setitem import create_set_item, add_food_to_setitem, add_setitem_to_setmenu
from model.customer import create_customer
from model.manager import create_manager
from model.dispatcher import create_dispatcher
from model.employee import create_employee
from loguru import logger


def seed_food_itemsWcategory():
    category_ids = seed_category()
    food_ids = seed_food_items()
    set_menu_ids = seed_set_menu()
    set_item_ids = seed_set_item()
    x = 0
    for category_id in category_ids:
        add_food_to_category({'food_id': food_ids[x], 'category_id': category_id})
        x = x + 1

    y = 0
    for set_menu_id in set_menu_ids:
        add_setitem_to_setmenu({'setitem_id': set_item_ids[y], 'setmenu_id': set_menu_id})
        y = y + 1

    for set_item_id in set_item_ids:
        add_food_to_setitem({'food_ids': food_ids, 'setitem_id': set_item_id})


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
    data = [
        {
            'name': 'Breakfast',
            'totalPrice': 100,
            'size': 10
        },
        {
            'name': 'Lunch',
            'totalPrice': 100,
            'size': 10
        },
        {
            'name': 'Dinner',
            'totalPrice': 100,
            'size': 10
        },
    ]
    set_menu_ids = []
    for row in data:
        set_menu_id = create_set_menu(row)
        set_menu_ids.append(set_menu_id)

    return set_menu_ids


def seed_set_item():
    data = ['Platter One', 'Platter Two', 'Platter Three']
    set_item_ids = []
    for name in data:
        set_item_id = create_set_item({'name': name})
        set_item_ids.append(set_item_id)

    return set_item_ids


def seed_customer():
    data = {
        'name': 'Saitama',
        'address': 'Okinawa',
        'email': 'saitama@gmail.com',
        'contactNumber': 123456,
        'password': 'password'
    }
    create_customer(data)


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
    create_employee(data)


def seed_dispatcher():
    data = {'name': 'genos', 'commission': 100.33}
    create_dispatcher(data)
