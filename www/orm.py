#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# reference: https://github.com/michaelliao/awesome-python3-webapp/blob/day-03/www/orm.py

import logging
import aiomysql


def log(sql, args=()):
    logging.basicConfig(level=logging.INFO)
    logging.info('SQL: {} with arguments: {}'.format(sql, args))

async def create_pool(loop, **kw):
    """
    创建一个全局的进程池；
    设置连接DB所需的各种参数；
    设置最小/最大连接数目，防止过多的连接导致系统资源消耗过多；
    :param loop: event loop
    :param kw: parameters to connect DBs
    :return:
    """
    logging.info('create database connection pool...')
    global __pool  # 把全局连接池__pool定义为一个全局变量
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),  # 主机地址
        port=kw.get('port', 3306),  # 连接端口号
        user=kw['user'],  # user name
        password=kw['password'],  # password
        db=kw['database'],  # DB name
        charset=kw.get('charset', 'utf8'),  # 设置字符集，默认utf8
        autocommit=kw.get('autocommit', True),  # 设置自动提交事务，默认打开
        maxsize=kw.get('maxsize', 10),  # 设置最大连接数，默认10个
        minsize=kw.get('minsize', 1),  # 设置最小连接数，默认1个
        loop=loop  # 传递一个事件循环实，不设置的话内部默认使用asyncio.get_event_loop()
    )

async def select(sql, args, size=None):
    """
    实现了SQL查询语句：SELECT；
    :param sql: SQL语句
    :param args: SQL语句中占位符(%s)对应的参数
    :param size: 返回记录的行数
    :return: 返回的记录
    """
    log(sql, args)
    global __pool  # 使用全局连接池__pool
    async with __pool.get() as conn:  # 从全局连接池中acquire一个连接，使用后自动释放(with)
        async with conn.cursor(aiomysql.DictCursor) as cur:  # 创建一个游标，返回一个由`dict`组成的`list`，使用后自动释放(with)
            # 使用带参数的方式执行SQL语句
            # 标准SQL语句的占位符使用的是`？`
            # MySQL的占位符是`%s`（和Python字符串格式化的占位符相同）
            # 考虑到兼容性，执行时才把`？`replace成`%s`再执行
            await cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs = await cur.fetchmany(size)  # fetch指定行数的记录
            else:
                rs = await cur.fetchall()  # fetch所有行记录
        logging.info('rows returned: {}'.format(len(rs)))
        return rs

async def execute(sql, args, autocommit=True):
    """
    实现了SQL操作语句：INSERT/UPDATE/DELETE；
    默认打开事务自动提交的功能；
    :param sql: SQL语句
    :param args: SQL语句中占位符(%s)对应的参数
    :param autocommit: 是否自动提交事务
    :return: 影响行数
    """
    log(sql)
    async with __pool.get() as conn:  # 从全局连接池中acquire一个连接，使用后自动释放(with)
        # 如果autocommit=False，则通过MySQL的begin方法显式地开启事务
        # begin()方法可参考：`https://github.com/aio-libs/aiomysql/blob/master/aiomysql/sa/connection.py`
        if not autocommit:
            await conn.begin()
        try:
            # 创建一个游标，返回一个由`dict`组成的`list`，使用后自动释放(with)
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # 使用带参数的方式执行SQL语句
                # 标准SQL语句的占位符使用的是`？`
                # MySQL的占位符是`%s`（和Python字符串格式化的占位符相同）
                # 考虑到兼容性，执行时才把`？`replace成`%s`再执行
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount  # 获得影响行数
            if not autocommit:
                await conn.commit()  # 显式提交
        except BaseException as e:
            # 执行出错时，回滚事务
            if not autocommit:
                await conn.rollback()
            raise
        return affected


def create_args_string(num):
    L = []
    for n in range(num):  # 根据占位符个数num生成`？`组成的list
        L.append('?')
    return ', '.join(L)  # 用`, `连接list的各元素得到一个str，如`?, ?, ?`


class Field(object):
    """
    定义一个数据库数据的基类；
    用于衍生各种ORM中数据库数据的类型;
    """
    def __init__(self, name, column_type, primary_key, default):
        self.name = name  # 字段的name
        self.column_type = column_type  # 字段的数据库数据类型
        self.primary_key = primary_key  # 是否是主键
        self.default = default  # 默认值

    def __str__(self):
        """
        用于print(instance)时打印构造字符串
        :return: 构造字符串
        """
        return '<{}, {}:{}>'.format(self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    """
    从基类Field继承，定义一个字符类；
    用StringField的实例化参数初始化基类Field；
    默认数据库数据类型为变长100字符；
    默认值：None
    """
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name=name, column_type=ddl, primary_key=primary_key, default=default)


class BooleanField(Field):
    """
    从基类Field继承，定义一个布尔类；
    用StringField的实例化参数初始化基类Field；
    数据库数据类型指定：boolean；
    默认值：False
    """
    def __init__(self, name=None, default=False):
        super().__init__(name=name, column_type='boolean', primary_key=False, default=default)


class IntegerField(Field):
    """
    从基类Field继承，定义一个整数类；
    用StringField的实例化参数初始化基类Field；
    数据库数据类型指定：bigint；
    默认值：0
    """
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name=name, column_type='bigint', primary_key=primary_key, default=default)


class FloatField(Field):
    """
    从基类Field继承，定义一个浮点数类；
    用StringField的实例化参数初始化基类Field；
    数据库数据类型指定：real；
    默认值：0.0
    """
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name=name, column_type='real', primary_key=primary_key, default=default)


class TextField(Field):
    """
    从基类Field继承，定义一个文本类；
    用StringField的实例化参数初始化基类Field；
    数据库数据类型指定：text；
    默认值：None
    """
    def __init__(self, name=None, default=None):
        super().__init__(name=name, column_type='text', primary_key=False, default=default)


class ModelMetaclass(type):
    """
    定义一个元类，用来实现定制类到数据库表的映射关系；
    从这个元类类生成的类，自然就实现了ORM(object relational mapping)
    """
    def __new__(cls, name, bases, attrs):
        # 如果类名字为`model`，则不做任何修改直接返回model类
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        table_name = attrs.get('__table__', None) or name  # 从类属性中查找__table__属性，作为数据表名，如果是None则以类名作为表名
        logging.info('found model: {} (table: {})'.format(name, table_name))
        mappings = dict()  # 记录实例的属性attrs和数据类型Field的对应关系
        fields = []  # 存储非主键的name
        primary_key = None
        for k, v in attrs.items():  # 迭代所有实例属性
            if isinstance(v, Field):  # 如果value的类型=Field
                logging.info('found mapping: {} ==> {}'.format(k, v))
                mappings[k] = v  # 向mapping中添加键值对{name: Field}
                if v.primary_key:  # 找到主键
                    if primary_key:  # 第n(n>1)次找到主键，抛出错误
                        raise BaseException('Duplicate primary key for field: %s' % k)
                    primary_key = k  # primary_key置位=主键name
                else:
                    fields.append(k)  # 记录非主键name到fields
        if not primary_key:  # 没有找到任何主键
            raise BaseException('Primary key not found.')
        for k in mappings.keys():  # 从属性attrs中删除copy到mapping中的键值对，不然直接访问`实例.attr`会得到映射到的Field对象，而不是期望得到的value了
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))  # 给非主键的字段名加上反引号，防止出现MySQL的关键字？
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系，即attrs到Fields
        attrs['__table__'] = table_name  # 表名
        attrs['__primary_key__'] = primary_key  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primary_key, ', '.join(escaped_fields), table_name)  # 主键和表名也加上反引号，而非主键因为需要用都好分割所以前面单独做了处理
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (table_name, ', '.join(escaped_fields), primary_key, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (table_name, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primary_key)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (table_name, primary_key)
        return type.__new__(cls, name, bases, attrs)  # 使用type生成目标类并返回


class Model(dict, metaclass=ModelMetaclass):
    """
    定义了一个模板类Model，它继承自dict，同时生成新类时受metaclass的控制；
    由于在Model内内忧定义__new__方法，所以从Model继承得到的子类会自动调用ModelMetaclass内的__new__方法，使得子类都能自动实现ORM
    """
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        """
        实现`实例.key`方式对属性的访问，前提是没有key属性存在，才能跳转执行此方法
        :param key: 属性key
        :return: key对应的value
        """
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        """
        同上getattr的实现
        :param key:
        :param value:
        :return:
        """
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        """
        find objects by where clause.
        添加类方法，对应查表，默认查整个表，可通过where limit设置查找条件
        :param where:
        :param args:
        :param kw:
        :return:
        """
        sql = [cls.__select__]  # sql语句存入一个列表中
        if where:  # 如果有where位置参数
            sql.append('where')
            sql.append(where)
        if args is None:  # 如果有args位置参数
            args = []
        orderBy = kw.get('orderBy', None)  # 获取orderBy排序条件
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)  # 获取limit条件
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql), args)  # 构造更新后的select语句，并执行，返回属性值[{},{},{}]
        return [cls(**r) for r in rs]  # 返回一个列表。每个元素都是一个Model实例，相当于一行记录

    @classmethod
    async def findNumber(cls, select_field, where=None, args=None):
        """
        find number by select and where.
        :param select_field:
        :param where:
        :param args:
        :return:
        """
        sql = ['select %s _num_ from `%s`' % (select_field, cls.__table__)]  # _num_是SQL的一个字段别名用法，AS关键字可以省略
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']  # 根据别名key取值

    @classmethod
    async def find(cls, pk):
        """
        类方法：根据主键查询一条记录
        :param pk:
        :return:
        """
        ' find object by primary key. '
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        """
        实例方法，映射插入记录
        :return:
        """
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warning('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        """
        实例方法，映射更新记录
        :return:
        """
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warning('failed to update by primary key: affected rows: %s' % rows)

    async def remove(self):
        """
        实例方法，映射根据主键删除记录
        :return:
        """
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warning('failed to remove by primary key: affected rows: %s' % rows)
