#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' cover module '

__author__ = 'Haifeng Kong'

from sys import exit

import pygame
from pygame.locals import *

import button
from config import *

# 变量#
cover_img_filename = "封面1.png"  # 封面背景文件

# 操作的按钮，第一列为按钮上显示的文字，第二列为操作的ID
buttonList = (
    ["新游戏", 0],
    ["读取进度", 1],
    ["选项", 2],
    ["退出", 3],
)


#################################################################
# 初始化，绘制背景，按钮和按钮上的文字，创建按钮的检测区域数组
#################################################################

def init():
    # 初始化界面
    if not pygame.get_init():
        pygame.init()
    screen = pygame.display.set_mode(SCREEN, 0, 32)

    # 绘制背景
    background = pygame.image.load(cover_img_filename)
    background = pygame.transform.scale(background, SCREEN)
    screen.blit(background, (0, 0))

    # 绘制按钮
    surf = button.init(buttonList, screen)

    # 合并图层
    screen.blit(surf, (0, 0))

    # 展示
    pygame.display.update()


def load():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # 退出按钮被按下
                exit()
            elif event.type == MOUSEBUTTONDOWN:  # 鼠标按键被按下
                func = button.checkButtonPress(pygame.mouse.get_pos())
                if func == 3:
                    exit()
                return func  # 返回按钮对应的操作


def test():
    while True:
        fu = load()
        if fu < 0:
            print("检测到鼠标点击，但未点击按钮。")
        else:
            print(buttonList[fu][0] + "按钮被点击。")


if __name__ == '__main__':
    test()
