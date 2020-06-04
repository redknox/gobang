#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' graphic module '

__author__ = 'Haifeng Kong'

from sys import exit

import pygame
from pygame.locals import *
from config import *

# 变量#
cover_img_filename = "封面1.png"  # 封面背景文件

# 操作的按钮，第一列为按钮上显示的文字，第二列为操作的ID
buttonList = (
    ["新游戏", 0],
    ["读取进度", 1],
    ["选项", 2],
    ["制作组", 3],
    ["退出", 4],
)


#################################################################
# 初始化，绘制背景，按钮和按钮上的文字，创建按钮的检测区域数组
#################################################################

def init():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN, 0, 32)
    # 绘制背景
    background = pygame.image.load(cover_img_filename)
    background = pygame.transform.scale(background, SCREEN)
    screen.blit(background, (0, 0))

    # 绘制按钮

    btnLineWidth = BTN_SIZE[1] + BTN_LINE_SPACING  # 每行按钮的总宽度（包含行间距）

    surface2 = screen.convert_alpha()  # 按钮为透明图层

    # 计算第一个按钮的左上角坐标
    btnNumbers = len(buttonList)  # 按钮总数
    btnUpLeftX = (WIDE - BTN_SIZE[0]) / 2  # 左上角X坐标
    btnUpLeftY = (WIDE - (BTN_SIZE[1] * btnNumbers + (btnNumbers - 1) * 50)) / 2  # 左上角Y坐标

    # 在画布上依次绘制按钮
    for i in range(btnNumbers):
        pygame.draw.rect(surface2, BTN_COLOR,
                         [btnUpLeftX,
                          btnUpLeftY + btnLineWidth * i,
                          BTN_SIZE[0],
                          BTN_SIZE[1]],
                         0)
        buttonList[i].append((btnUpLeftX, btnUpLeftY + btnLineWidth * i))
    screen.blit(surface2, (0, 0))

    # 绘制按钮上的文字

    font = pygame.font.Font(FONT_FILE, BTN_FONT_SIZE)  # 读取字体
    font.set_bold(True)

    for i in range(btnNumbers):
        surface = font.render(buttonList[i][0], False, BTN_TXT_COLOR)  # 渲染文字
        fontRect = surface.get_rect()  # 取得渲染后画板的尺寸
        # 根据画板的尺寸把文字贴在背景上
        screen.blit(surface, (
            (WIDE - fontRect[2]) / 2,
            (btnUpLeftY + (BTN_SIZE[1] - fontRect[3]) / 2) + btnLineWidth * i + 2))  # 实际应用将文字向下修正两个像素，否则显得文字在按钮上偏上

    pygame.display.update()


##############################################################
# 根据传入的坐标，判断是否在按钮范围内，如果在，则返回按钮的操作ID，否则返回-1
##############################################################


def checkButton(pos):
    for bu in buttonList:
        if bu[2][0] < pos[0] < bu[2][0] + BTN_SIZE[0]:
            if bu[2][1] < pos[1] < bu[2][1] + BTN_SIZE[1]:
                return bu[1]
    return -1


def load():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # 退出按钮被按下
                exit()
            elif event.type == MOUSEBUTTONDOWN:  # 鼠标按键被按下
                func = checkButton(pygame.mouse.get_pos())  # 取得鼠标点击按钮的编号，如果未点击按钮，则返回-1
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
