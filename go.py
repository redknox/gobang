#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 五子棋程序  """

__author__ = 'Haifeng Kong'

import cover
import new
import option
import play

if __name__ == '__main__':
    f = cover.load()
    while f != 2:
        if f == 0:
            f = new.load()
        elif f == 1:
            f = option.load()
        elif f == 3:
            f = play.load()
        elif f == 5:
            f = cover.load()
