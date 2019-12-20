########################################################################################################################
# 五子棋
# V1 实现交互界面：点击屏幕后自动落子，并计算胜负。
# TODO: 将判断胜负的功能抽象为函数，将代码按功能拆分
########################################################################################################################
import pygame
import sys
from pygame.locals import *
import abc

########################################################################################################################
FPS = 50  # 帧数
WIDE = 771  # 工作区为长宽为751的正方形
LINES = 15  # 标准五子棋棋盘，有十五条线
cellWidth = (WIDE - 20) // LINES  # 格子宽度
current_po = (-1, -1)  # 最后一个落子位置，（-1，-1）表示当前数据不可用
flag = 0  # 同步标志，0为初始化，1为已落子，2为等待人工落子，3为等待AI落子


#####################
# 设置标志,因为对象无法直接操作全局变量，特别用这个函数来操作
# 输入：int id 状态类型：0 初始化 1 已经落子，等待判定 2 等待人工落子 3 等待AI落子
#####################

def set_flag(id):
    global flag
    flag = id


#####################
#
# 棋手类.所有棋手的基类
#
#####################

class Player(metaclass=abc.ABCMeta):
    id = 0  # 棋手ID，黑棋为1，白棋为2
    name = ''  # 棋手姓名
    type = 0  # 玩家类型，2 为真人玩家，3为ai玩家 这个类型等同于状态，表示等待真人玩家落子和等待AI玩家落子

    # 落子程序,抽象方法，必须在子类中实现
    @abc.abstractmethod
    def move(self):
        pass


#####################
#
# 真人棋手类
#
#####################

class Human_player(Player):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.type = 2  # 指定当前玩家为真人玩家

    def move(self):
        set_flag(2)  # 只需要修改标志位为2，等待系统接收键盘点击事件即可


#####################
# 绘制棋子
# input: x,y 落子在棋盘上的位置，color 落子颜色
# output: 无
#####################
def draw_piece(po, id):
    # 不进行合法性检查了
    x = po[0] * cellWidth + 10
    y = po[1] * cellWidth + 10
    if (id == 1):
        windowSurface.blit(go_piece_black, (x, y))
    else:
        windowSurface.blit(go_piece_white, (x, y))


#####################
# 获胜判定
# input x,y 落子位置,player 玩家编号,可选值是1或2
# output ture/false 是否获胜
#####################
def judge_victory(po, player):
    # 分别计算横、竖线、左斜、右斜四条直线上连成一线棋子的总数，如果有5个则比赛获胜
    # 先计算从落子出发一个方向的格子是否和落子有一样颜色的棋子，是的话count+1，继续判断该方向下一个格子，直到碰到第一个没有棋子或者有棋子颜色不同的格子
    # 然后计算落子另一个方向的棋子，算法同前
    for x, y in ((-1, 1), (1, 1), (1, 0), (0, 1)):  # 4条直线，右斜、左斜、垂直、水平
        count = 1  # 当前直线上连续子的个数，落子后为1

        for direction in (1, -1):  # 两个方向
            x, y = x * direction, y * direction

            current_x, current_y = po[0] + x, po[1] + y  # 计算在当前直线上，沿着当前当前方向下一个格子的位置
            if current_x < 0 or current_y < 0 or current_x >= LINES or current_y >= LINES:  # 如果超出棋盘则退出当前循环，换下一方向或者换下一条直线
                break

            while a[current_x][current_y] == player:
                count += 1
                if count == 5:
                    return True  # 返回获胜
                current_x += x
                current_y += y
                if current_x < 0 or current_y < 0 or current_x >= LINES or current_y >= LINES:
                    break

    return False  # 返回未获胜


#####################
# 点击落子
#####################
def u_click(mouse_x, mouse_y):
    if mouse_x < 25 or mouse_y < 20 or mouse_x > 761 or mouse_y > 761:
        return (-1, -1)

    # 根据点击位置计算落子位置
    x = (mouse_x - 10) // cellWidth
    y = (mouse_y - 10) // cellWidth

    # 判断当前位置上是否有棋子，有的话本次点击无效
    if a[x][y] != 0:
        return (-1, -1)

    return (x, y)


if __name__ == '__main__':
    pygame.init()
    windowSurface = pygame.display.set_mode((WIDE, WIDE), 0, 32)
    pygame.display.set_caption('孔海峰的五子棋练习')

    # 读取棋盘、棋子的资源文件
    go_piece_black = pygame.image.load("go_piece_black.png").convert_alpha()
    go_piece_white = pygame.image.load("go_piece_white.png").convert_alpha()
    background = pygame.image.load("gobang_plate.jpeg")  # 读取背景图片
    background = pygame.transform.scale(background, (WIDE, WIDE))  # 调整背景图片大小
    windowSurface.blit(background, (0, 0))  # 绘制背景
    # 读取黑白棋图片
    go_piece_black = pygame.transform.scale(go_piece_black, (50, 50))
    go_piece_white = pygame.transform.scale(go_piece_white, (50, 50))
    # 初始化棋盘
    pygame.display.update()

    # 初始化棋盘数组
    a = []
    for i in range(LINES):
        a.append([])
        for j in range(LINES):
            a[i].append(0)  # 棋盘上每个格子初始为空

    # 初始化时钟
    clock = pygame.time.Clock()

    # 初始化玩家

    player1 = Human_player(1, 'kong')

    player2 = Human_player(2, 'Haifeng')

    currentPlayer = player1

    # flag 是标志，0表示初始化，1表示当前玩家已经落子，2表示等待人工落子，3表示等待AI落子
    flag = currentPlayer.type

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # 如果当前状态为等待玩家落子
                if flag == 2:
                    mouse_x, mouse_y = event.pos
                    current_po = u_click(mouse_x, mouse_y)

                    if current_po == (-1, -1):
                        break
                    else:
                        flag = 1  # 将状态设置为已经落子

        # 如果已经落子
        if flag == 1:
            # 重绘棋盘
            draw_piece(current_po, currentPlayer.id)
            pygame.display.update()

            a[current_po[0]][current_po[1]] = currentPlayer.id  # 将当前玩家落子存入数组

            # 获胜判定
            if judge_victory(current_po, currentPlayer.id):
                print(currentPlayer.name + "我赢了，哈哈哈哈哈哈啊哈哈！")

            # TODO：记录棋型

            # 转换玩家
            if currentPlayer == player1:
                currentPlayer = player2
            else:
                currentPlayer = player1

            # 当前玩家走子
            currentPlayer.move()

        time_passed = clock.tick(FPS)
