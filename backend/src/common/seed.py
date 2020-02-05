#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.food import create_food
from model.category import create_category, add_food_item
from model.customer import create_customer
from model.manager import create_manager
from model.dispatcher import create_dispatcher
from model.employee import create_employee
from loguru import logger


def seed_food_items():
    data = [
        {
            'name': 'Chicken Burger',
            'status': True,
            'price': 10,
            'description': 'This is a chicken burger',
            'unit': 100,
            'category': 'Chicken'
        },
        {
            'name': 'Fish Burger',
            'status': True,
            'price': 10,
            'description': 'This is a fish burger',
            'unit': 100,
            'category': 'Fish'
        },
        {
            'name': 'Tiramisu',
            'status': True,
            'price': 10,
            'description': 'This is a tiramisu',
            'unit': 100,
            'category': 'Desert'
        },
        {
            'name': 'Pepsi',
            'status': True,
            'price': 10,
            'description': 'This is a pepsi',
            'unit': 100,
            'category': 'Beverages'
        },
    ]

    for row in data:
        food_id = create_food(row)
        try:
            if food_id is not None:
                category_id = create_category({
                    'name': row['category'],
                    'foodItems': [food_id]
                })
        except Exception as e:
            logger.error(e)


def seed_customer():
    data = {
        'name': 'Saitama',
        'address': 'Okinawa',
        'email': 'saitama@gmail.com',
        'contactNumber': 123456
    }
    create_customer(data)


def seed_manager():
    data = {
        'name': 'Atomic Samurai',
        'nric': 8888888,
        'contactNumber': 123456,
        'dateJoined': '2020-01-20 12:18:23 UTC',
        'startDate': '2020-01-22 12:18:23 UTC',
        'status': True,
        'gender': 'Male'
    }
    create_manager(data)


def seed_employee():
    data = {
        'name': 'garo',
        'nric': 9999999,
        'contactNumber': 123456,
        'dateJoined': '2020-01-20 12:18:23 UTC',
        'status': True,
        'gender': 'Male'
    }
    create_employee(data)


def seed_dispatcher():
    data = {'name': 'genos', 'commission': 100.33}
    create_dispatcher(data)
