#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
url handlers
"""
import time
import json
import hashlib
import re
from aiohttp import web

from framework import get, post
from models import User, Blog, Comment, next_id
from apierror import Page, APIError, APIValueError, APIPermissionError

import logging
logging.basicConfig(level=logging.INFO)

COOKIE_NAME = 'session'
_COOKIE_KEY = 'growing up is a gradual separation'


def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()


def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


def user2cookie(user, max_age):
    """
    cookies加密
    :param user:
    :param max_age:
    :return:
    """
    expires = str(int(time.time() + max_age)) # 计算过期时间，以字符串返回
    s = '%s-%s-%s-%s' %(user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)


async def cookie2user(cookie_str):
    """
    cookies解密
    :param cookie_str:
    :return:
    """
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():  # cookie过期
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None


@get('/')
def index(request):
    summary = 'Reformat Code. For selections, you can also convert the selection using the "To spaces" function. I usually just use it via the ctrl-shift-A then find "To Spaces" from there. ctrl + shift + A => open pop window to select options, select to spaces to convert all tabs as space, or to tab to convert as tab.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs,
        '__user__': request.__user__
    }


@get('/api/users')
async def api_get_users():
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    return dict(users=users)


_reEmail = re.compile(r'^[0-9a-z\.\-\_]+\@[0-9a-z\-\_]+(\.[0-9a-z\-\_]+){1,4}$')
_reSha1 = re.compile(r'^[0-9a-f]{40}$')  # SHA1不够安全，后续需升级


@get('/register')
def register():
    return {'__template__': 'register.html'}


@get('/signin')
def signin():
    return {'__template__': 'signin.html'}


@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r


@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }


@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }


@get('/api/blogs')
async def api_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)


@get('/api/blogs/{id}')
async def api_get_blog(*, id):
    blog = await Blog.find(id)
    return blog


@post('/api/users')
async def api_register_user(*, email, name, passwd):
    """kw var : email, name, passwd"""
    if not email or not _reEmail.match(email):
        raise APIValueError('email')
    if not name or not name.strip():  # 移除字符串头尾的空格
        raise APIValueError('name')
    if not passwd or not _reSha1.match(passwd):
        raise APIValueError('passwd')
    users = await User.findAll('email=?', [email])  # 对应 where, args 参数
    if len(users) > 0:
        raise APIError('register failed', email, 'Email is already in use')
    uid = next_id()
    sha1Passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, email=email, passwd=hashlib.sha1(sha1Passwd.encode('utf-8')).hexdigest(), name=name.strip(), image='about:blank')
    await user.save()
    # session cookie
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True) # httponly指定JS不能获取COOKIE
    user.passwd = '******'  # 清理内存中的passwd
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8') # 转换成JSON格式
    return r


@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email is not existed.')
    user = users[0]
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True) # httponly指定JS不能获取COOKIE
    user.passwd = '******'  # 清理内存中的passwd
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8') # 转换成JSON格式
    return r


@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog