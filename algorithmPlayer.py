#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a algorithm player module '

import numpy as np

from playerClass import Player

__author__ = 'Haifeng Kong'


#####################
#
#  算法棋手类
#
#####################

class AlgorithmPlayer(Player):
    # 棋型表，这里只列出了冲棋型，因为活棋型实际只是冲棋型的一个子集，配合冲活标志可以检测活棋，所以就没有单独列出
    CHONGSI = (15, 23, 27, 29, 30)  # 冲四
    MIANSAN = (7, 11, 13, 14, 19, 21, 22, 25, 26, 28)  # 闷三
    MIANER = (3, 5, 6, 9, 10, 12, 17, 18, 20, 24)  # 闷二
    MINYI = (16, 8, 4, 2, 1)  # 闷一，术语里没有这个叫法，为了计算特意加上
    # 棋型集和
    qxmc = (CHONGSI, MIANSAN, MIANER, MINYI)

    # 将上表整理成下面的列表进行计算
    QXL = (0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4)

    # 方向集合，1,0 表示水平向右，0，1表示水平向下，1，1表示从左上到右下，2 表示从左下到右上
    direction = ((1, 0), (0, 1), (1, 1), (1, -1))

    # 区域集合，整个棋盘分为4个区域，不同的区域可以检测的方向不同，第一个数组为x值取值范围，第二个数组为y值取值范围，第三个数组为可以检测的方向的id
    # 例如：第一区域为(0,0)到(11,4),这个区域内可以检测的方向为0，1，2，既水平、垂直、左上到右下
    area = [
        [[0, 11], [0, 4], [0, 1, 2]],
        [[0, 11], [4, 11], [0, 1, 2, 3]],
        [[0, 11], [11, 15], [0, 3]],
        [[11, 15], [0, 11], [1]]
    ]

    #################################################################
    # 初始化:设置玩家颜色
    #################################################################
    def __init__(self, color):
        self.pieceColor = color
        self.name = '算法'
        self.winText = '你输了'
        self.chessLibrary = [[[], [], [], [], []], [[], [], [], [], []]]  # 棋型库，用来存放各种棋型,每次落子之前要重新计算全部棋型

    #################################################################
    # 根据传入的棋盘表，计算当前的棋型库，归纳黑白双方目前存在的冲/活四，眠三，活二和活一，供算法决策
    #################################################################
    def createChessLibrary(self, chessRecord):
        self.chessLibrary = [[[], [], [], [], []], [[], [], [], [], []]]  # 棋型库，用来存放各种棋型,每次落子之前要重新计算全部棋型
        # 便利棋盘上每个连续的5个连续位置，判断是否构成棋型
        for squr in self.area:  # 不同方向棋型的4块区域
            for x in range(squr[0][0], squr[0][1]):
                for y in range(squr[1][0], squr[1][1]):
                    for i in squr[2]:  # 每块区域的特定方向
                        count = 0  # 计数器
                        tx = x
                        ty = y
                        blackChess = 0
                        whiteChess = 0
                        empty = 0
                        emptyCross = []
                        while count < 5:  # 从当前位置，特定方向连续取五个位置，统计黑白空三种情况的个数
                            blackChess = blackChess * 2
                            whiteChess = whiteChess * 2
                            if chessRecord[tx][ty] == -1:
                                empty += 1
                                emptyCross.append((tx, ty))
                            elif chessRecord[tx][ty] == 0:
                                blackChess = blackChess + 1
                            elif chessRecord[tx][ty] == 1:
                                whiteChess = whiteChess + 1

                            tx += self.direction[i][0]
                            ty += self.direction[i][1]
                            count += 1

                        if blackChess > 0 and whiteChess > 0:  # 当五个位置同时有黑白棋，则不构成任何棋型
                            continue

                        if empty == 5:  # 5个位置全部为空位，不构成任何棋型
                            continue

                        # 将对应棋型记录进入棋型库
                        if blackChess > 0:
                            self.chessLibrary[0][self.QXL[blackChess]].append([(x, y), i, blackChess, emptyCross])
                        else:
                            self.chessLibrary[1][self.QXL[whiteChess]].append([(x, y), i, whiteChess, emptyCross])

    #################################################################
    # 落子程序，先调用createChessLibrary函数构建棋型库
    # 依据先防后攻击的原则，也就是先放对方的活四/冲四,再凑自己的活四/冲四,再防对方的眠三，再凑自己的棉三
    # 找到最有威胁的攻防棋型，然后记录该棋型的落子位置，并便利剩余所有棋型库的落子位置，进行加权
    # 最后从权值最高的落子位置中选择个进行落子
    #################################################################
    def go(self, pieceRecord, lastPieceGo):
        # 更新棋型库
        self.createChessLibrary(pieceRecord)
        # 先防后供
        A = self.pieceColor  # 攻击
        D = (A + 1) % 2  # 防守
        aiFlag = True  # 追加、检测标志，如果追加标志为0，则将空位追加到empty库，否则，只计算empty库的权值
        ecCount = {}
        for i in (4, 3, 2, 1):  # 按照冲四/活四、冲三、活二、活一的顺序
            for j in (D, A):  # 先防守再攻击
                if len(self.chessLibrary[j][i]) > 0:
                    for k in self.chessLibrary[j][i]:  # 取每一个棋型的空格
                        if aiFlag:
                            for ks in k[3]:
                                if ks in ecCount.keys():
                                    ecCount[ks] += 1
                                else:
                                    ecCount[ks] = 1
                        else:
                            for cs in k[3]:
                                if cs in ecCount.keys():
                                    ecCount[cs] += 1
                    aiFlag = False
        # todo: 现在仅仅读取了落点库第一个推荐项，后面可以加上禁手、已有三维棋型等功能。
        return (max(ecCount, key=ecCount.get))


# 测试

if __name__ == '__main__':
    qx = np.full((15, 15), -1)
    qx[3][4] = 0
    '''
    qx[0][1] = 1
    qx[0][2] = 1
    qx[0][3] = 1
    qx[0][4] = 1
    qx[4][1] = 1
    qx[4][2] = 1
    qx[4][3] = 1
    qx[1][0] = 1
    qx[2][0] = 1
    qx[3][0] = 1
    qx[4][0] = 1
    qx[1][4] = 1
    qx[2][4] = 1
    qx[3][4] = 1
    '''
    print(qx)
    test = AlgorithmPlayer(1)
    print(test.go(qx, (0, 0)))
