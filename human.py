#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a human player module '

__author__ = 'Haifeng Kong'

import pygame
from pygame.locals import *

from config import *

###############################################
# 人类棋手模块，本模块实现点击棋盘计算落子位置、判断当前位置是否可以落子、可以的话返回落子信息
###############################################
NAME = "玩家"  # 玩家的名称
WIN_TEXT = "你赢了!"  # 玩家胜利后显示的信息


#####################
# 根据鼠标点击的位置在棋盘上的位置落子
#####################
def go(pieceRecord):
    mouse = []
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # 退出按钮被按下
                exit()
            elif event.type == MOUSEBUTTONDOWN:  # 鼠标按键被按下
                mouse = (pygame.mouse.get_pos())

                tx = (mouse[0] - 10) // CELL_WIDTH
                ty = (mouse[1] - 10) // CELL_WIDTH
                if pieceRecord[tx][ty] != -1:
                    print("已经有子了！")
                    continue
                else:
                    return tx, ty


if __name__ == '__main__':
    if not pygame.get_init():
        pygame.init()
    screen = pygame.display.set_mode(SCREEN, 0, 32)
    while True:
        print(go())
