#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' new module '

__author__ = 'Haifeng Kong'

from sys import exit

import pygame
from pygame.locals import *

import button
from config import *

# 变量#
new_img_filename = "新建背景.jpg"  # 封面背景文件

# 操作的按钮，第一列为按钮上显示的文字，第二列为操作的ID
buttonList = (
    ["算法对手", 3],
    ["返回", 5]
)

# 背景图层
background = ''


#################################################################
# 初始化，绘制背景，按钮和按钮上的文字，创建按钮的检测区域数组
#################################################################

def init(screen):
    # 初始化界面
    if not pygame.get_init():
        pygame.init()
    # screen = pygame.display.set_mode(SCREEN, 0, 32)

    # 绘制背景
    global background
    background = pygame.image.load(new_img_filename)
    background = pygame.transform.scale(background, SCREEN)
    screen.blit(background, (0, 0))

    # 绘制按钮
    button.init(buttonList)
    surf = button.drawBtn(screen)

    # 合并图层
    screen.blit(surf, (0, 0))

    # 展示
    pygame.display.update()


def load(screen):
    init(screen)
    onButton = -1
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # 退出按钮被按下
                exit()
            elif event.type == MOUSEBUTTONDOWN:  # 鼠标按键被按下
                func = button.checkButtonPress(pygame.mouse.get_pos())
                if func != -1:
                    return func  # 返回按钮对应的操作
            elif event.type == MOUSEMOTION:
                func = button.checkButtonPress(pygame.mouse.get_pos())
                if func != onButton:
                    surf = button.drawBtn(screen, func)
                    screen.blit(background, (0, 0))
                    screen.blit(surf, (0, 0))
                    pygame.display.update()
                    onButton = func


def test():
    if not pygame.get_init():
        pygame.init()
    screen = pygame.display.set_mode(SCREEN, 0, 32)
    while True:
        fu = load(screen)
        print(fu)


if __name__ == '__main__':
    test()
