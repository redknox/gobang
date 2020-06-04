#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 五子棋程序  """

__author__ = 'Haifeng Kong'

import cover

if __name__ == '__main__':
    f = cover.load()
    print(f)
    if f == 0:
        pass  # 打开新建页面
    elif f == 1:
        pass  # 打开选项页面
    elif f == 2:
        pass  # 打开读取页面
