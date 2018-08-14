#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
url handlers
"""


from framework import get, post
from models import User, Comment, Blog, next_id
import re, time, json, logging, hashlib, base64, asyncio


@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }


@get('/api/users')
async def api_get_users():
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    return dict(users=users)
