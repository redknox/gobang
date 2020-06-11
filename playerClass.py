#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Haifeng Kong'

import abc


# 所有棋手类的抽象类

class Player(metaclass=abc.ABCMeta):
    pieceColor = 0  # 玩家棋子颜色
    name = ''  # 棋手姓名
    winText = ''  # 玩家获胜后展示的文字

    # 落子程序,抽象方法，必须在子类中实现
    @abc.abstractmethod
    def go(self):
        pass

