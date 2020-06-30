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
background = ''  # 背景图层


#################################################################
# 初始化，绘制背景，按钮和按钮上的文字，创建按钮的检测区域数组
#################################################################

def init(screen, config):
    # 初始化界面
    if not pygame.get_init():
        pygame.init()

    # 绘制背景
    global background
    background = pygame.image.load(new_img_filename)
    background = pygame.transform.scale(background, SCREEN)
    screen.blit(background, (0, 0))

    # 构造按钮组
    buttonList = []
    if config["music_on"]:
        buttonList.append(["音乐：开", 7])
    else:
        buttonList.append(["音乐：关", 7])
    if config["show_order"]:
        buttonList.append(["落子顺序：显示", 6])
    else:
        buttonList.append(["落子顺序：隐藏", 6])

    buttonList.append(["返回", 5])

    # 绘制按钮
    button.init(buttonList)
    surf = button.drawBtn(screen)

    # 合并图层
    screen.blit(surf, (0, 0))

    # 展示
    pygame.display.update()


def load(screen, config):
    init(screen, config)
    onButton = -1
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # 退出按钮被按下
                exit()
            elif event.type == MOUSEBUTTONDOWN:  # 鼠标按键被按下
                func = button.checkButtonPress(pygame.mouse.get_pos())
                if func == 6:
                    config['show_order'] = not config['show_order']
                    init(screen, config)
                elif func == 7:
                    config['music_on'] = not config['music_on']
                    if config['music_on']:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.fadeout(2000)
                    init(screen, config)
                elif func == 8:
                    config['sound_on'] = not config['sound_on']
                    init(screen, config)
                elif func == 5:
                    return gameConfig  # 返回按钮对应的操作
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
