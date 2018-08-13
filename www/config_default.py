#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Default configurations.
"""

configs = {
    'debug': True,
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'db': 'ablog'
    },
    'session': {
        'secret': 'ablog'
    }
}