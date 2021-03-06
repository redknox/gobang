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
    ["选项", 1],
    ["退出", 2],
)

backGround = ''  # 背景图层


#################################################################
# 初始化，绘制背景，按钮和按钮上的文字，创建按钮的检测区域数组
#################################################################

def init(screen):
    # 初始化界面
    if not pygame.get_init():
        pygame.init()
    # screen = pygame.display.set_mode(SCREEN, 0, 32)

    # 绘制背景
    global backGround
    backGround = pygame.image.load(cover_img_filename)
    backGround = pygame.transform.scale(backGround, SCREEN)
    screen.blit(backGround, (0, 0))

    # 绘制按钮
    button.init(buttonList)
    surf = button.drawBtn(screen)

    # 合并图层
    screen.blit(surf, (0, 0))

    # 展示
    pygame.display.update()


##############################################################
# 初始化屏幕，监控鼠标点击事件，如果点击在按钮上则返回按钮ID
# think: 每个屏幕监控的操作不同，有的监控鼠标按键，有的同事还监控其他事件，不适宜抽象成函数
###############################################################
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
                    screen.blit(backGround, (0, 0))
                    screen.blit(surf, (0, 0))
                    pygame.display.update()
                    onButton = func


def test():
    screen = pygame.display.set_mode(SCREEN, 0, 32)
    while True:
        fu = load(screen)
        if fu < 0:
            print("检测到鼠标点击，但未点击按钮。")
        else:
            print(buttonList[fu][0] + "按钮被点击。")


if __name__ == '__main__':
    test()
