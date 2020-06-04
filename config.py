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

# 按钮相关
BTN_SIZE = (222, 66)  # 按钮大小
BTN_COLOR = (102, 102, 102, 204)  # 按钮颜色
BTN_LINE_SPACING = 50  # 按钮行间距
BTN_FONT_SIZE = 28
BTN_TXT_COLOR = (255, 255, 255)

# 文字相关
FONT_FILE = "方正硬笔楷书简体.ttf"


def test():
    print('每秒刷新数 FPS=' + str(FPS))
    print('屏幕宽度 WIDTH=' + str(WIDE))
    print('棋盘线数 LINES=' + str(LINES))


if __name__ == '__main__':
    test()
