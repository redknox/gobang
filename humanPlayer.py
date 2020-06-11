#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

import pygame
from pygame.locals import *

from config import *
from playerClass import Player

__author__ = 'Haifeng Kong'


#####################
#
# 真人棋手类
#
#####################

class HumanPlayer(Player):
    def __init__(self, color):
        self.pieceColor = color
        self.name = '玩家'
        self.winText = '你赢了'

    def go(self, pieceRecord, lastPieceGo):
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
    pass
