########################################################################################################################
# 五子棋
# V1 实现交互界面：点击屏幕后自动落子，并计算胜负。
# TODO: 将判断胜负的功能抽象为函数，将代码按功能拆分
########################################################################################################################
import pygame
import sys
from pygame.locals import *

########################################################################################################################
FPS = 50  # 帧数
WIDE = 951  # 工作区为长宽为951的正方形
LINES = 19  # 标准围棋盘，有十九条线
cellWidth = WIDE // LINES  # 格子宽度
W = WIDE // cellWidth  #
# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

a = []  # 构造数组a放置每个格子的信息
for i in range(LINES):
    a.append([])
    for j in range(LINES):
        a[i].append(0)  # 棋盘上每个格子初始为空

pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WIDE, WIDE), 0, 32)
pygame.display.set_caption('gobang')
windowSurface.fill(YELLOW)
# 画线
for i in range(0, LINES + 1):
    postion = i * cellWidth
    pygame.draw.line(windowSurface, BLACK, (0, postion), (949, postion), 1)
    pygame.draw.line(windowSurface, BLACK, (postion, 0), (postion, 949), 1)

pygame.display.update()

# 初始化
# 注意，当循环开始后，会先更换当前玩家，所以将当前玩家设置为白棋玩家
currentColor = WHITE
player = 2
debug = []

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            unit_x = mouse_x // cellWidth
            unit_y = mouse_y // cellWidth
            mouse_x = unit_x * cellWidth + cellWidth // 2
            mouse_y = unit_y * cellWidth + cellWidth // 2

            # 判断当前位置上是否有棋子，有的话本次点击无效
            if a[unit_x][unit_y] != 0:
                break

            # 转换玩家
            # 可以在这里写
            if player == 2:
                currentColor = BLACK
                player = 1
            else:
                currentColor = WHITE
                player = 2

            a[unit_x][unit_y] = player  # 将当前玩家落子存入数组

            # 更新棋盘显示
            pygame.draw.circle(windowSurface, currentColor, (mouse_x, mouse_y), cellWidth // 2 - 2, 0)
            pygame.draw.circle(windowSurface, BLACK, (mouse_x, mouse_y), cellWidth // 2 - 2, 1)
            pygame.display.update()

            count = 1  # 当前落子后练成一线的棋子总数
            max = 0  # 各个方向上连成一线棋子的最大值

            # 分别计算横、竖线、左斜、右斜四条直线上连成一线棋子的总数，如果有5个则比赛获胜
            # 先计算从落子出发一个方向的格子是否和落子有一样颜色的棋子，是的话count+1，继续判断该方向下一个格子，直到碰到第一个没有棋子或者有棋子颜色不同的格子
            # 然后计算落子另一个方向的棋子，算法同前
            for x, y in ((-1, 1), (1, 1), (1, 0), (0, 1)):  # 4条直线，右斜、左斜、垂直、水平
                count = 1

                for direction in (1, -1):  # 两个方向
                    x, y = x * direction, y * direction

                    current_x, current_y = unit_x + x, unit_y + y  # 计算在当前直线上，沿着当前当前方向下一个格子的位置
                    if current_x < 0 or current_y < 0 or current_x >= LINES or current_y >= LINES:  # 如果超出棋盘则退出当前循环，换下一方向或者换下一条直线
                        break

                    while a[current_x][current_y] == player:
                        count += 1
                        if count == 5:
                            print('player', player, 'win!')
                        current_x += x
                        current_y += y
                        if current_x < 0 or current_y < 0 or current_x >= LINES or current_y >= LINES:
                            break

                if count > max:  # 保存最大的单行连续棋子数
                    max = count

            print(max)

    time_passed = clock.tick(FPS)
