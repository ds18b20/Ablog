#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import asyncio
import uuid
from orm import create_pool, Model, StringField, BooleanField, FloatField, TextField

"""
Models for user, blog, comment.
"""


def next_id():
    """
    生成不重复的id
    :return: id --> str
    """
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    # 类的属性
    # 只是为了提供这些attrs给元类，在元类内部转换成name到Field的映射关系，然后把这个关系保存在元类的__mapping__属性中
    # 最终这些attrs会被pop掉，不然在实例中访问这些属性时，会默认找到class属性中的attr到Field的键值对，而不是希望的attr到value的键值对
    __table__ = 'users'  # 映射到表名用的

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)


class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)


class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)


async def test(loop):
    await create_pool(loop=loop, user='admin', password='admin', database='ablog')
    user_1 = {
        'name': 'Holmes',
        'email': 'Holmes@example.com',
        'password': 'aaaaaa',
        'image': 'image'
    }
    user_2 = {
        'name': 'Wason',
        'email': 'Wason@example.com',
        'password': 'bbbbbb',
        'image': 'image'
    }
    u_1 = User(**user_1)
    await u_1.save()
    u_2 = User(**user_2)
    await u_2.save()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    # loop.run_forever()
