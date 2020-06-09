#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 五子棋程序  """

__author__ = 'Haifeng Kong'

import pygame

# 载入各个组件
import cover  # 封面和主菜单
import new  # 新建游戏菜单
import option  # 选项菜单
import play  # 游戏界面
from config import *

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SCREEN, 0, 32)
    f = cover.load(screen)
    while f != 2:  # 当退出按钮被按下，则退出循环结束游戏
        if f == 0:  # 当新建游戏按钮被按下，调起新建游戏模块
            f = new.load(screen)
        elif f == 1:  # 当选项按钮被按下，调起选项模块
            f = option.load(screen)
        elif f == 3:  # 当开始游戏按钮被按下，调起游戏模块
            f = play.load(screen)
        elif f == 5:  # 当返回按钮被按下，调起封面主菜单模块。
            f = cover.load(screen)
    # TODO：显示结束游戏画面
