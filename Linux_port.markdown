# Linux port
Linux系的os内查看端口使用状况的方式记录如下：
## netstat

查看已经连接的服务端口（ESTABLISHED）

`netstat -a`

查看所有的服务端口（LISTEN，ESTABLISHED）

`netstat -ap`

## 查看指定端口
- netstat结合grep命令：
`netstat -ap | grep 8080`
- 或者使用lsof命令：
`lsof -i:9000`

## 关闭端口
kill -9 PID号

> kill就是给某个进程id发送了一个信号。默认发送的信号是SIGTERM，而kill -9发送的信号是SIGKILL，即exit。exit信号不会被系统阻塞，所以kill -9能顺利杀掉进程。

# Reference
https://www.jianshu.com/p/4441c966583f