#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' new module '

__author__ = 'Haifeng Kong'

from sys import exit

import numpy as np
import pygame
from pygame.locals import *

import button
from algorithmPlayer import AlgorithmPlayer
from config import *
from humanPlayer import HumanPlayer

######################################################################
# 本模块是五子棋程序的核心调度模块，本模块的功能主要有：
# 1、绘制棋盘、棋子、落子顺序、提示等信息。
# 2、分别调用不同的棋手模块获得落子信息。
# 3、胜负判定
# 具体的下棋算法，在各个不同的棋手模块内实现。例如，人类玩家在humanPlayer模块内实现，算法玩家在algorithm模块
# 内实现，AI玩家在ai模块内实现。
#####################################################################


# 变量#
new_img_filename = "gobang_plate.jpeg"  # 封面背景文件
WIN = False  # 取胜标志，当某方判胜时改标志为True
winPiece = []  # 决胜棋位置，用于最终显示获胜提示
background = ''  # 背景图层
sufPiece = ''  # 棋子图层
sufPieceOrder = ''  # 棋子顺序图层
sufOthers = ''  # 其他信息图层
sufFont = ''  # 文字图层
fontCount = ''  # 显示落子顺序的字体
pieceBlack = ''  # 黑色棋子图层
pieceWhite = ''  # 白色棋子图层
pieceColor = ''  # 落子图层数组

# 棋局记录
pieceRecord = []  # 记录棋局，没有落子为-1，落黑子为0，落白子为1

# 玩家数组，内含两个玩家对象，默认第一个为执黑先行玩家，第二个为执白玩家
player = []

# 操作的按钮，第一列为按钮上显示的文字，第二列为操作的ID
buttonList = (
    ["再来一局", 0],
    ["返回", 2]
)

# 背景图层
background = ''

# 游戏配置
gameConfig = ''


#################################################################
# 初始化，绘制背景，按钮和按钮上的文字，创建按钮的检测区域数组
#################################################################

def init(screen):
    if not pygame.get_init():
        pygame.init()

    # 将变量设为初始值
    global WIN, background, pieceRecord, player, CUR_PIECE_COLOR, fontCount
    WIN = False  # 设置获胜标志为否
    CUR_PIECE_COLOR = BLACK_PIECE  # 设置当前玩家为黑棋

    fontCount = pygame.font.Font(FONT_FILE, 20)  # 读取字体

    # 初始化两个玩家
    # todo: 待AI玩家开发完毕，在这里将执白玩家设置成AI玩家
    player1 = HumanPlayer(BLACK_PIECE)
    player2 = AlgorithmPlayer(WHITE_PIECE)

    player = (player1, player2)  # 初始化玩家信息

    # 初始化棋局数组
    pieceRecord = np.full((LINES, LINES), -1)

    # 绘制背景
    global background
    background = pygame.image.load(new_img_filename)
    background = pygame.transform.scale(background, SCREEN)
    screen.blit(background, (0, 0))

    # 初始化棋子图层

    global sufPiece, sufOthers, sufPieceOrder, pieceColor
    pieceBlack = pygame.image.load("go_piece_black.png").convert_alpha()
    pieceWhite = pygame.image.load("go_piece_white.png").convert_alpha()
    pieceBlack = pygame.transform.scale(pieceBlack, (PIECE_WIDTH, PIECE_HEIGHT))
    pieceWhite = pygame.transform.scale(pieceWhite, (PIECE_WIDTH, PIECE_HEIGHT))

    pieceColor = (pieceBlack, pieceWhite)  # 将棋子图层放在数组中，用于在展示时切换

    sufPiece = screen.convert_alpha()  # 创建棋子透明图层
    sufPieceOrder = screen.convert_alpha()  # 创建展示棋子顺序的透明图层
    sufOthers = screen.convert_alpha()  # 创展示其他信息的透明图层

    # 显示棋盘
    pygame.display.update()


# 落子后重绘棋子层，顺序层和其他层
def drawPiece(screen):
    global PIECE_COUNT
    PIECE_COUNT = PIECE_COUNT + 1
    # 重绘棋子，因五子棋不会移动棋子，直接在原图层上增绘最新落下的棋子,而不用重绘全部棋子

    x = CUR_PIECE_LOCATION[0] * CELL_WIDTH + 10
    y = CUR_PIECE_LOCATION[1] * CELL_WIDTH + 10
    sufPiece.blit(pieceColor[CUR_PIECE_COLOR], (x, y))

    screen.blit(background, (0, 0))  # 重绘背景可以排除之前的所有干扰，尤其是others图层上的临时性信息
    screen.blit(sufPiece, (0, 0))  # 绘制棋子图层

    # 绘制其他图层

    if gameConfig['show_order']:  # 如果配置了显示落子顺序，则重绘落子顺序层
        # TODO：在这里写将顺序文字写到相应图层上的代码

        # 绘制文字
        if CUR_PIECE_COLOR != 0:
            sufFont = fontCount.render(str(PIECE_COUNT), False, (0, 0, 0))  # 渲染文字
        else:
            sufFont = fontCount.render(str(PIECE_COUNT), False, (255, 255, 255))  # 渲染文字

        fontRect = sufFont.get_rect()  # 取得渲染后画板的尺寸

        # 调整文字显示位置

        x = x + (PIECE_WIDTH - fontRect[2]) // 2
        y = y + (PIECE_HEIGHT - fontRect[3]) // 2

        # 合并文字图层
        sufPiece.blit(sufFont, (x, y))

        # pygame.draw.circle(sufPiece, (0, 0, 255), (x + CELL_WIDTH // 2, y + CELL_WIDTH // 2), 10)
        screen.blit(sufPiece, (0, 0))
        pass
    if SHOW_GUIDE:  # 如果配置了显示其他信息层，则重绘其他信息层
        # TODO：在这里写将辅助信息写到相应图层上的代码，本层每次下棋都要重绘
        screen.blit(sufOthers, (0, 0))
        pass
    pygame.display.update()


# 判断胜负
def judgeVictory():
    # 判断是否已经填满棋盘,todo: 后面可以写一个计数器，统计落子为225枚是直接白棋判胜。
    full = True
    for i in range(LINES):
        if -1 in pieceRecord[i]:
            full = False
            break
    if full:
        # 在这里写强制白棋获胜的代码
        global CUR_PIECE_COLOR
        CUR_PIECE_COLOR = (CUR_PIECE_COLOR + 1) % 2  # 因为棋盘上有225空位，那么下最后一个子的人一定是黑棋，判定白棋获胜可以直接交换当前玩家。
        return True
    # TODO：判断当前落子是否下出禁手，如出禁手则直接判对方获胜

    # 判胜算法：在四个方向上（水平，垂直，左斜，右斜），探测落子位置一侧的位置是否有与落子颜色相同的棋子，
    # 有则计数器加一，重复一直到：
    # 1、总数为5，判胜；
    # 2、遇到一个对方棋子或空位；
    # 3、遇到边界；
    # 然后开始探测落子另外一个方向上是否有同色棋子。重复之前步骤。
    # 结果有两个：1、计数器达到5，判胜；2、遇到对方棋子/空位/边界。都能够结束循环。

    direction = ((0, 1), (1, 0), (1, 1), (1, -1))  # 四个方向
    global winPiece
    for d in direction:
        count = 1  # 计数器，达到5时判胜
        winPiece = []  # 清空旧棋型
        for curDir in (-1, 1):
            cx, cy = CUR_PIECE_LOCATION  # 当前探测位置
            winPiece.append((cx, cy))
            cx, cy = cx + d[0] * curDir, cy + d[1] * curDir
            while pieceRecord[cx][cy] == CUR_PIECE_COLOR:
                count += 1
                winPiece.append((cx, cy))
                if count == 5:  # 如果有5连直接判胜
                    print(winPiece)
                    return True
                cx = cx + d[0] * curDir
                if cx < 0 or cx >= LINES:
                    break
                cy = cy + d[1] * curDir
                if cy < 0 or cy >= LINES:
                    break
    return False


# 判断是否点击屏幕
def mouseClick():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                return pygame.mouse.get_pos()


################################
# 核心功能
# 1、初始化游戏
# 2、调用当前玩家的落子程序
# 3、绘制
# 4、胜负判定
# 5、通过按钮显示是否再来一盘或退出
################################
def load(screen, config):
    # 初始化游戏
    init(screen)
    global gameConfig
    gameConfig = config
    # 初始化玩家
    # PLAYER1.init(BLACK_PIECE),将玩家1初始化为黑棋玩家
    # PLAYER2.init(WHITE_PIECE),将玩家2初始化成为白棋玩家,对于机器玩家来说，黑棋白棋策略不同，所以要先定义

    global CUR_PIECE_LOCATION, CUR_PIECE_COLOR, WIN

    while True:  # 双方轮流落子，直到决出胜负
        # 调用棋手模块go程序，取得棋手给出的落子位置
        CUR_PIECE_LOCATION = player[CUR_PIECE_COLOR].go(pieceRecord,
                                                        CUR_PIECE_LOCATION)  # 每个棋手模块必须有一个go()函数，返回一个棋盘上的位置，作为落子的的地垫
        # 检测落子位置是否合法,合法的话将落子信息记录到落子信息表，否则的话重新调用 TODO：AI棋手要具有判断落子是否合法的能力
        if pieceRecord[CUR_PIECE_LOCATION[0], CUR_PIECE_LOCATION[1]] != -1:
            continue
        else:
            pieceRecord[CUR_PIECE_LOCATION[0], CUR_PIECE_LOCATION[1]] = CUR_PIECE_COLOR

        print(pieceRecord.T)

        # 绘制棋子
        drawPiece(screen)

        # 判胜，如果获胜则退出当前循环，否则继续换下一位棋手落子
        if judgeVictory():
            break
        # 切换当前玩家
        CUR_PIECE_COLOR = (CUR_PIECE_COLOR + 1) % 2

    # -------------------------------------------

    # TODO:在决胜棋型上标记红色

    # -------------------------------------------
    for wp in winPiece:
        pygame.draw.circle(sufPiece, (255, 0, 0),
                           (wp[0] * CELL_WIDTH + 10 + CELL_WIDTH // 2, wp[1] * CELL_WIDTH + 10 + CELL_WIDTH // 2), 10)
    screen.blit(sufPiece, (0, 0))

    # 显示胜负信息
    # 绘制文字
    font = pygame.font.Font(FONT_FILE, 150)  # 读取字体
    sufFont = font.render(player[CUR_PIECE_COLOR].winText, False, (0, 255, 0))  # 渲染文字
    fontRect = sufFont.get_rect()  # 取得渲染后画板的尺寸

    # 调整文字显示位置
    x = (WIDE - fontRect[2]) / 2
    y = 180

    # 合并文字图层
    screen.blit(sufFont, (x, y))

    # -------------------------------------------
    # 绘制按钮
    button.init(buttonList, (BTN_ARRANGED_VERTICALLY, BTN_ON_BOTTOM_CENTER))
    surf = button.drawBtn(screen)

    # 合并图层并显示
    screen.blit(surf, (0, 0))
    pygame.display.update()

    # -------------------------------------------
    while True:  # 根据点击的按钮做出相应的处理
        buttonPress = button.checkButtonPress(mouseClick())
        if buttonPress != -1:
            if buttonPress == 2:  # 重新开局
                return 5
            elif buttonPress == 0:  # 退出游戏
                return 3
            break


if __name__ == '__main__':
    if not pygame.get_init():
        pygame.init()
    screen = pygame.display.set_mode(SCREEN, 0, 32)
    load(screen)
