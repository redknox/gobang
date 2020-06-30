#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' button module '

__author__ = 'Haifeng Kong'

from sys import exit

import pygame
from pygame.locals import *

from config import *

hotArea = []  # 按钮的点击热区数组,里面放有菜单的所有信息，菜单文字，ID，位置，大小


################################################################################
# 初始化按钮
# 输入：buttonList 一个button的数组，格式为（"按钮上的文字",id),id必须唯一
#      screen 需要绘制按钮图片的screen，不同screen的图层，在合并时会产生一些透明的问题
#      btnArrange button的排列方式和位置，默认为按钮垂直排列，位于屏幕正中
# 输出：hotArea数组，里面放有所有菜单项的菜单文字，ID，位置，大小
################################################################################

def init(buttonList, btnArrange=BTN_ON_DEFAULT):
    global hotArea
    hotArea = []  # 清空之前产生的数据

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
        # 根据排列方式依次计算按钮的位置，并将按钮信息放入hotArea组
    for i in range(btnNumbers):
        btnX = btnUpLeftX + btnHorizontalWidth * i
        btnY = btnUpLeftY + btnVerticalWidth * i
        hotArea.append((buttonList[i][0], buttonList[i][1], (btnX, btnY, BTN_SIZE[0], BTN_SIZE[1])))

    return hotArea


##################################################################################
# 绘制屏幕
# 从hotArea数组里依次取出相关信息绘制数组到一个透明的图层上。
# 输入：screen: pygame.screen类型，需要绘制的画框
#      mouseOnButton:int，需要高亮绘制背景的按钮ID
# 输出：一个pygame透明图层，可以覆盖在背景上
##################################################################################
def drawBtn(screen, mouseOnButton=-1):
    if not pygame.get_init():
        pygame.init()
    btnSurface = screen.convert_alpha()  # 创建一个透明图层

    font = pygame.font.Font(FONT_FILE, BTN_FONT_SIZE)  # 读取字体
    font.set_bold(True)

    for btn in hotArea:
        # 当前按钮的左上角坐标
        # 绘制按钮
        if mouseOnButton == btn[1]:
            pygame.draw.rect(btnSurface, BTN_ON_COLOR, btn[2], 0)
        else:
            pygame.draw.rect(btnSurface, BTN_COLOR, btn[2], 0)

        # 绘制按钮文字
        fntSurface = font.render(btn[0], False, BTN_TXT_COLOR)  # 渲染文字
        fontRect = fntSurface.get_rect()  # 取得渲染后画板的尺寸

        # 将文字图层合并到按钮图层合适的位置，文字位置计算基于按钮的左上角坐标和按钮宽度与高度，这样可以适应不同布局的按钮排列
        btnSurface.blit(fntSurface, (
            btn[2][0] + (btn[2][2] - fontRect[2]) / 2,
            btn[2][1] + (btn[2][3] - fontRect[3]) / 2 + 2))  # 实际应用将文字向下修正两个像素，否则显得文字在按钮上偏上

    return btnSurface


##################################################################################
# 点击和鼠标当前位置检测，根据传入的坐标，检测是否位于按钮上。是的话返回按钮的ID，否的话返回-1。此函数必须在按钮图层初始化后才可以调用，否则会
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
def test(btnArrange=1, btnOn=4, mouseOnBtn=9999):
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

    init(buttonList, (btnArrange, btnOn))
    surface = drawBtn(screen)

    screen.blit(surface, (0, 0))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # 退出按钮被按下
                exit()
            elif event.type == MOUSEMOTION:  # 当移动鼠标时判断是否在按钮上，是的话则高亮按钮，移开后恢复原状
                pos = pygame.mouse.get_pos()
                func = checkButtonPress(pos)
                if mouseOnBtnId != func:
                    surface = drawBtn(screen, func)
                    screen.blit(surface, (0, 0))
                    pygame.display.update()
                    mouseOnBtnId = func

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
