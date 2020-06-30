#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' config informaiton '

__author__ = 'Haifeng Kong'

# 常量
# 工作区
FPS = 50  # 帧数
WIDE = 771  # 工作区为长宽为771的正方形
SCREEN = (WIDE, WIDE)  # 屏幕大小
LINES = 15  # 标准五子棋棋盘，有十五条线
CELL_WIDTH = (WIDE - 20) // LINES  # 格子宽度
PIECE_WIDTH = 50  # 棋子宽度
PIECE_HEIGHT = 50  # 棋子高度

# 按钮相关
BTN_SIZE = (222, 66)  # 按钮大小
BTN_COLOR = (102, 102, 102, 204)  # 按钮颜色
BTN_ON_COLOR = (204, 204, 204, 204)  # 鼠标在按钮上时的颜色
BTN_LINE_SPACING = 50  # 按钮行间距
BTN_FONT_SIZE = 28
BTN_TXT_COLOR = (255, 255, 255)

# 按钮距离上下左右的边距
BTN_PADDING_LEFT = 50
BTN_PADDING_RIGHT = 50
BTN_PADDING_TOP = 50
BTN_PADDING_BOTTOM = 150

# 按钮排列方式
BTN_ARRANGED_VERTICALLY = 1
BTN_ARRANGED_HORIZONTALLY = 0

# 按钮对齐方式
BTN_ON_TOP_LEFT = 0
BTN_ON_TOP_CENTER = 1
BTN_ON_TOP_RIGHT = 2
BTN_ON_MIDDLE_LEFT = 3
BTN_ON_CENTER = 4
BTN_ON_MIDDLE_RIGHT = 5
BTN_ON_BOTTOM_LEFT = 6
BTN_ON_BOTTOM_CENTER = 7
BTN_ON_BOTTOM_RIGHT = 8

# 默认按钮排列方式
BTN_ON_DEFAULT = (BTN_ARRANGED_VERTICALLY, BTN_ON_CENTER)

# 文字相关
FONT_FILE = "方正硬笔楷书简体.ttf"

# 棋子配置
BLACK_PIECE = 0  # 黑棋的编号为0
WHITE_PIECE = 1  # 白棋的编号为1

########################################################
# 变量
# 下面的变量在程序中可以更改
########################################################

# 系统变量
MAIN_SCREEN = ''  # 系统画板

# 配置信息
SHOW_ORDER = False  # 是否显示落子顺序，True时，在每个棋子上绘制落步数
SHOW_GUIDE = False  # 是否显示提示，显示的话，提示自己的攻防建议

# 声音信息
MUSIC_ON = True
SOUND_ON = False

gameConfig = {
    "music_on": True,
    "sound_on": False,
    "show_order": True
}

# 玩家信息，需要在棋局初始化时，初始化为对应的模块对象
PLAYER1 = ''  # 执黑先行玩家
PLAYER2 = ''  # 执白后行玩家
PLAYERS = (PLAYER1, PLAYER2)  # 玩家数组，用于计算当前玩家

# 当前落子信息
CUR_PIECE_LOCATION = (0, 0)  # 当前落子信息
CUR_PIECE_COLOR = (BLACK_PIECE)  # 当前落子颜色
PIECE_COUNT = 0  # 落子总数


def test():
    print('每秒刷新数 FPS=' + str(FPS))
    print('屏幕宽度 WIDTH=' + str(WIDE))
    print('棋盘线数 LINES=' + str(LINES))


if __name__ == '__main__':
    test()
