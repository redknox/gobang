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
WIDE = 771  # 工作区为长宽为751的正方形
LINES = 15  # 标准围棋盘，有十九条线
cellWidth = (WIDE - 20) // LINES  # 格子宽度
W = WIDE // cellWidth  #
# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

if __name__ == '__main__':
    print('main')


#####################
# 绘制棋子
# input: x,y 落子在棋盘上的位置，color 落子颜色
#####################
def draw_piece(x, y, color):
    # 不进行合法性检查了
    x = x * cellWidth + cellWidth // 2 + 10
    y = y * cellWidth + cellWidth // 2 + 10
    pygame.draw.circle(windowSurface, color, (x, y), cellWidth // 2 - 2, 0)
    pygame.draw.circle(windowSurface, BLACK, (x, y), cellWidth // 2 - 2, 1)


#####################
# 判断是否获胜
# input x,y 落子位置,player 玩家编号
# output ture/false 是否获胜
#####################
def judge_victory(unit_x, unit_y, player):
    max = 0  # 各个方向上连成一线棋子的最大值

    # 分别计算横、竖线、左斜、右斜四条直线上连成一线棋子的总数，如果有5个则比赛获胜
    # 先计算从落子出发一个方向的格子是否和落子有一样颜色的棋子，是的话count+1，继续判断该方向下一个格子，直到碰到第一个没有棋子或者有棋子颜色不同的格子
    # 然后计算落子另一个方向的棋子，算法同前
    for x, y in ((-1, 1), (1, 1), (1, 0), (0, 1)):  # 4条直线，右斜、左斜、垂直、水平
        count = 1  # 当前直线上连续子的个数，落子后为1

        for direction in (1, -1):  # 两个方向
            x, y = x * direction, y * direction

            current_x, current_y = unit_x + x, unit_y + y  # 计算在当前直线上，沿着当前当前方向下一个格子的位置
            if current_x < 0 or current_y < 0 or current_x >= LINES or current_y >= LINES:  # 如果超出棋盘则退出当前循环，换下一方向或者换下一条直线
                break

            while a[current_x][current_y] == player:
                count += 1
                if count == 5:
                    print('player', player, 'win!')
                    return True
                current_x += x
                current_y += y
                if current_x < 0 or current_y < 0 or current_x >= LINES or current_y >= LINES:
                    break

        if count > max:  # 保存最大的单行连续棋子数
            max = count

    print(max)
    return False


a = []  # 构造数组a放置每个格子的信息
for i in range(LINES):
    a.append([])
    for j in range(LINES):
        a[i].append(0)  # 棋盘上每个格子初始为空

pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WIDE, WIDE), 0, 32)
pygame.display.set_caption('孔海峰的五子棋练习')

# 绘制背景
background = pygame.image.load("gobang_plate.jpeg")
background = pygame.transform.scale(background, (WIDE, WIDE))
windowSurface.blit(background, (0, 0))
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
        # 等待玩家落子
        if event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # 合法性检查
            if mouse_x < 25 or mouse_y < 20 or mouse_x > 761 or mouse_y > 761:
                break
            # 根据点击位置计算落子位置
            unit_x = (mouse_x - 10) // cellWidth
            unit_y = (mouse_y - 10) // cellWidth

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

            # 落子
            draw_piece(unit_x, unit_y, currentColor)
            pygame.display.update()

            a[unit_x][unit_y] = player  # 将当前玩家落子存入数组

            if judge_victory(unit_x, unit_y, player):
                print("我赢了，哈哈哈哈哈哈啊哈哈！")


    time_passed = clock.tick(FPS)
