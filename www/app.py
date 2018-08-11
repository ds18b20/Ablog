#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Reference: www.liaoxuefeng.com

import asyncio
from aiohttp import web
# from aiohttp import web_runner
import logging
logging.basicConfig(level=logging.INFO)


'''
async web application.
'''


def index(request):
    """
    响应函数，根据request返回html代码
    :param request: 请求内容
    :return: html code
    """
    return web.Response(body=b'<h1>Hello World!</h1>', content_type='text/html')

async def init(loop):
    """
    生成web对象；
    绑定响应函数到路由；
    设置监听端口；
    :param loop: 事件循环
    :return: web对象
    """
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8080)
    logging.info('server started at http://127.0.0.1:8080...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
# loop.run_forever()
