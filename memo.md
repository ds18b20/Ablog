# PyCharm
## Cannot find reference 'xxx' in __init__.py - Python / Pycharm
https://stackoverflow.com/questions/23248017/cannot-find-reference-xxx-in-init-py-python-pycharm

# Python
## __new__ and __init__
https://stackoverflow.com/questions/674304/why-is-init-always-called-after-new

## Python inspect模块参数类型kind的整理
https://blog.csdn.net/weixin_35955795/article/details/53053762
https://blog.csdn.net/heartroll/article/details/79268493

## url quote/unquote
http://www.cnblogs.com/kaituorensheng/p/3927000.html

---

# MySQL
## 事务
> 在 MySQL 命令行的默认设置下，事务都是自动提交的，即执行 SQL 语句后就会马上执行 COMMIT 操作。因此要显式地开启一个事务务须使用命令 BEGIN 或 START TRANSACTION，或者执行命令 SET AUTOCOMMIT=0，用来禁止使用当前会话的自动提交。

http://www.runoob.com/mysql/mysql-transaction.html


## 谈谈数据库连接池的原理
https://blog.csdn.net/shuaihj/article/details/14223015

## mysql中key 、primary key 、unique key 与index区别
http://zccst.iteye.com/blog/1697043

---
# Deployment
## supervisor+gunicorn部署python web项目
https://blog.csdn.net/qq_37049050/article/details/78500906

## Fabric EC2 instance
https://abhishek-tiwari.com/interacting-with-tagged-ec2-instances-using-fabric/

---
# python中aiohttp request 的处理过程解析
https://yq.aliyun.com/ziliao/25438
http://blog.sina.com.cn/s/blog_6b665ba40102x4o3.html

# Ngnix设置
## error while attempting to bind on address ('127.0.0.1', 9000): address already in use
https://stackoverflow.com/questions/19071512/socket-error-errno-48-address-already-in-use
> $ ps -fA | grep python
  501 81651 12648   0  9:53PM ttys000    0:00.16 python -m SimpleHTTPServer
  
> kill 81651

## 502 Bad Gateway
sudo /etc/init.d/nginx restart

reference:
http://otiai10.hatenablog.com/entry/2013/10/10/095213

# Python locale error: unsupported locale setting
Ubuntu下使用pip install安装包时，出现locale设置错误
> export LC_ALL="en_US.UTF-8"
> export LC_CTYPE="en_US.UTF-8"

> sudo dpkg-reconfigure locales


reference:

https://stackoverflow.com/questions/14547631/python-locale-error-unsupported-locale-setting

## How To Install MySQL on Ubuntu 16.04
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04
