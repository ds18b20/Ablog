#!/usr/bin/env python
# -*- coding=utf-8 -*-

import time

file_path = '/home/ubuntu/time'
fm = '%Y-%m-%d %X'


def get_time():
    while 1:
        now_time = time.strftime(fm, time.localtime())
        with open(file_path, 'a') as fp:
            fp.write(now_time)
            fp.write('\n')
        time.sleep(5)

if __name__ == '__main__':
    get_time()
