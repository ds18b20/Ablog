# MySQL 删除数据库
执行删除数据库的命令会直接删除该数据库的所有数据，故应做好备份工作。

## 使用drop方式
登入SQL环境下可以使用drop命令删除数据库：
mysql>`drop database <database name>`

## 使用mysqladmin删除
这种方式不要求进入SQL环境，直接在Terminal下实现：
[root@host]# `mysqladmin -u root -p drop <databese name>`
接下来会提示输入密码，并且确认是否确定删除。
