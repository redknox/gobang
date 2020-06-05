#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' button module '

__author__ = 'Haifeng Kong'

from sys import exit

import pygame
from pygame.locals import *

from config import *

hotArea = []  # 按钮的点击热区数组


################################################################################
# 初始化按钮
# 输入：buttonList 一个button的数组，格式为（"按钮上的文字",id),id必须唯一
#      screen 需要绘制按钮图片的screen，不同screen的图层，在合并时会产生一些透明的问题
#      btnArrange button的排列方式和位置，默认为按钮垂直排列，位于屏幕正中
# 输出：一个绘制有按钮和按钮文字的透明图层，可以根据需要叠加到screen上
################################################################################

def init(buttonList, screen, btnArrange=BTN_ON_DEFAULT):
    global hotArea
    hotArea = []  # 清空之前产生的数据
    if not pygame.get_init():
        pygame.init()
    btnSurface = screen.convert_alpha()  # 创建一个透明图层

    font = pygame.font.Font(FONT_FILE, BTN_FONT_SIZE)  # 读取字体
    font.set_bold(True)

    btnNumbers = len(buttonList)  # 获得按钮总数

    # 计算水平方向上的按钮数，按钮间距数，用于后面按钮位置的计算
    btnVerticalNumbers = 1  # 垂直方向上按钮总数
    btnVerticalSpaceNumbers = 0  # 垂直方向上按钮间距总数
    btnHorizontalNumbers = 1  # 水平方向上按钮总数
    btnHorizontalSpaceNumbers = 0  # 水平方向上按钮间距总数

    btnVerticalWidth = BTN_SIZE[1] + BTN_LINE_SPACING  # 垂直方向上按钮+间距的宽度
    btnHorizontalWidth = BTN_SIZE[0] + BTN_LINE_SPACING  # 水平方向上按钮+间距宽度

    if btnArrange[0] == BTN_ARRANGED_VERTICALLY:
        btnVerticalNumbers = btnNumbers
        btnVerticalSpaceNumbers = btnNumbers - 1
        btnHorizontalWidth = 0
    else:
        btnHorizontalNumbers = btnNumbers
        btnHorizontalSpaceNumbers = btnNumbers - 1
        btnVerticalWidth = 0

    # 计算按键组合的高度和宽度,水平宽度等于水平方向上按钮宽度和加上水平方向上按钮间距和，垂直也一样
    btnGroupWidth = BTN_SIZE[0] * btnHorizontalNumbers + BTN_LINE_SPACING * btnHorizontalSpaceNumbers
    btnGroupHeight = BTN_SIZE[1] * btnVerticalNumbers + BTN_LINE_SPACING * btnVerticalSpaceNumbers

    btnUpLeftX = btnUpLeftY = 0  # 按钮组左上角坐标

    # 计算第一个按钮的左上角坐标，按照按钮组位于field左上、中上、右上、左中、正中、右中、左下、中下、右下9中方式
    if btnArrange[1] == BTN_ON_TOP_LEFT:
        btnUpLeftX = BTN_PADDING_LEFT
        btnUpLeftY = BTN_PADDING_TOP
    elif btnArrange[1] == BTN_ON_TOP_CENTER:
        btnUpLeftX = (WIDE - btnGroupWidth) / 2
        btnUpLeftY = BTN_PADDING_TOP
    elif btnArrange[1] == BTN_ON_TOP_RIGHT:
        btnUpLeftX = WIDE - btnGroupWidth - BTN_PADDING_RIGHT
        btnUpLeftY = BTN_PADDING_TOP
    elif btnArrange[1] == BTN_ON_MIDDLE_LEFT:
        btnUpLeftX = BTN_PADDING_LEFT
        btnUpLeftY = (WIDE - btnGroupHeight) / 2
    elif btnArrange[1] == BTN_ON_CENTER:
        btnUpLeftX = (WIDE - btnGroupWidth) / 2
        btnUpLeftY = (WIDE - btnGroupHeight) / 2
    elif btnArrange[1] == BTN_ON_MIDDLE_RIGHT:
        btnUpLeftX = WIDE - btnGroupWidth - BTN_PADDING_RIGHT
        btnUpLeftY = (WIDE - btnGroupHeight) / 2
    elif btnArrange[1] == BTN_ON_BOTTOM_LEFT:
        btnUpLeftX = BTN_PADDING_LEFT
        btnUpLeftY = WIDE - btnGroupHeight - BTN_PADDING_BOTTOM
    elif btnArrange[1] == BTN_ON_BOTTOM_CENTER:
        btnUpLeftX = (WIDE - btnGroupWidth) / 2
        btnUpLeftY = WIDE - btnGroupHeight - BTN_PADDING_BOTTOM
    elif btnArrange[1] == BTN_ON_BOTTOM_RIGHT:
        btnUpLeftX = WIDE - btnGroupWidth - BTN_PADDING_RIGHT
        btnUpLeftY = WIDE - btnGroupHeight - BTN_PADDING_BOTTOM

    # 在画布上依次绘制按钮
    for i in range(btnNumbers):
        # 当前按钮的左上角坐标
        btnX = btnUpLeftX + btnHorizontalWidth * i
        btnY = btnUpLeftY + btnVerticalWidth * i
        # 绘制按钮
        pygame.draw.rect(btnSurface, BTN_COLOR,
                         [btnX,
                          btnY,
                          BTN_SIZE[0],
                          BTN_SIZE[1]],
                         0)

        # 记录按钮的点击热点区
        hotArea.append((buttonList[i][0], buttonList[i][1], (btnX, btnY)))

        # 绘制按钮文字
        fntSurface = font.render(buttonList[i][0], False, BTN_TXT_COLOR)  # 渲染文字
        fontRect = fntSurface.get_rect()  # 取得渲染后画板的尺寸

        # 将文字图层合并到按钮图层合适的位置，文字位置计算基于按钮的左上角坐标和按钮宽度与高度，这样可以适应不同布局的按钮排列
        btnSurface.blit(fntSurface, (
            btnX + (BTN_SIZE[0] - fontRect[2]) / 2,
            btnY + (BTN_SIZE[1] - fontRect[3]) / 2 + 2))  # 实际应用将文字向下修正两个像素，否则显得文字在按钮上偏上

    return btnSurface


##################################################################################
# 点击检测，根据传入的坐标，检测是否位于按钮上。是的话返回按钮的ID，否的话返回-1。此函数必须在按钮图层初始化后才可以调用，否则会
# 抛出异常。
# 输入:(x,y)格式的坐标信息
# 输出:int 按钮的id或者-1
##################################################################################
def checkButtonPress(pos):
    if len(hotArea) != 0:
        for bu in hotArea:
            if bu[2][0] < pos[0] < bu[2][0] + BTN_SIZE[0]:
                if bu[2][1] < pos[1] < bu[2][1] + BTN_SIZE[1]:
                    return bu[1]
        return -1
    else:
        raise Exception("checkButtonPress()操作必须先用init(buttonList)初始化button图层！")


# 测试
def test(btnArrange=1, btnOn=4):
    buttonList = (
        ["新游戏", 0],
        ["读取进度", 1],
        ["退出", 2],
        ["制作组", 3]
    )

    # 测试没初始化时是否正常报错
    # checkButtonPress((3, 2))

    screen = pygame.display.set_mode(SCREEN, 0, 32)
    cover_img_filename = "封面1.png"  # 封面背景文件
    background = pygame.image.load(cover_img_filename)
    background = pygame.transform.scale(background, SCREEN)
    screen.blit(background, (0, 0))

    surface = init(buttonList, screen, (btnArrange, btnOn))

    screen.blit(surface, (0, 0))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # 退出按钮被按下
                exit()
            elif event.type == MOUSEBUTTONDOWN:  # 鼠标按键被按下
                func = checkButtonPress(pygame.mouse.get_pos())  # 取得鼠标点击按钮的编号，如果未点击按钮，则返回-1
                return func  # 返回按钮对应的操作


if __name__ == '__main__':
    # 用不同的按钮排序方式和位置测试
    for i in range(2):  # 测试按钮组纵向排列和横向排列
        for j in range(9):  # 测试9种按钮组方位
            while True:
                re = test(i, j)
                print(re)
                if re == 2:  # 当按的是退出按钮时，退出当前页
                    break
