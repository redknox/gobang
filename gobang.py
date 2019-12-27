########################################################################################################################
# 五子棋
# V1 实现交互界面：点击屏幕后自动落子，并计算胜负。
# TODO: 将判断胜负的功能抽象为函数，将代码按功能拆分
########################################################################################################################
import pygame
import sys
from pygame.locals import *
import abc
import random

########################################################################################################################
FPS = 50  # 帧数
WIDE = 771  # 工作区为长宽为751的正方形
LINES = 15  # 标准五子棋棋盘，有十五条线
cellWidth = (WIDE - 20) // LINES  # 格子宽度
current_po = (-1, -1)  # 最后一个落子位置，（-1，-1）表示当前数据不可用
flag = 0  # 同步标志，0为初始化，1为已落子，2为等待人工落子，3为等待AI落子

# 棋型表，这里只列出了冲棋型，因为活棋型实际只是冲棋型的一个子集，配合冲活标志可以检测活棋，所以就没有单独列出

CHONGSI = (15, 23, 27, 29, 30)  # 冲四
MIANSAN = (7, 11, 13, 14, 19, 21, 22, 25, 26, 28)  # 闷三
MIANER = (3, 5, 6, 9, 10, 12, 17, 18, 20, 24)  # 闷二
MINYI = (16, 8, 4, 2, 1)  # 闷一，术语里没有这个叫法，为了计算ai特意加上

# 定义术语，AC表示构造己方冲棋，0 4棋型，1 3棋型 2 2棋型，如 AH0 表示用己方活4赢得比赛，DC2表示防守对方场上的冲二棋型，阻止构成冲三
A = 1  # 进攻，构造自己的棋型
D = 0  # 防守, 破坏对方的棋型
C = 1  # 冲棋
H = 0  # 活棋

# 棋型集和
qxmc = (CHONGSI, MIANSAN, MIANER, MINYI)

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

# 棋盘表，用于存储当前棋盘情况，下标为x,y的坐标值，表示棋盘上的眼位，值为落子情况。0为没落子，1为玩家1的黑棋，2为玩家2的黑棋。
a = []

# 棋型库，里面存储了检测出的所有棋型供双方博弈时参考。下标数据结构为：
# b[玩家id][活冲标志][活冲类]
# 玩家id： 0 Player1 1 Player2
# 活冲标志：0 活棋型 1 冲棋型（闷棋型）
# 活冲类：0 活四或者冲四 1 活三或者闷三 2 活二或者闷二
# 例如：b[1][0][1]=表示玩家2白棋玩家的"活三"棋
# 值：[(开始位置坐标),方向，棋型）
# 开始位置：棋型开始的地方，（x,y)
# 方向：代表方向的id
# 棋型：实际的棋型数字

b = []


#####################
#
# 根据传入的棋型id计算可以落子的位置
# 输入： int id,huo_flag 冲活标志，True为活，False为冲
# 输出： 可以落子的数组
#####################
def get_allow_persion(id):
    st = (16, 8, 4, 2, 1)
    i = 0
    re = []
    for ssi in st:
        if id & ssi == 0:
            re.append(i)
        i = i + 1
    return re

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


####################
#
# AiRnd 攻击和防守时，同等级别的棋型随机选取一个进行。例如同时存在两个活三棋，则随机取一个攻防
#
####################

class AI_rnd_player(Player):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.type = 3  # 等待AI落子

    def move_on(self, pro):
        rest = get_allow_persion(pro[2])
        print(rest)

        persi = random.randint(0, len(rest) - 1)
        print(persi)

        x = pro[0][0] + direction[pro[1]][0] * rest[persi]
        y = pro[0][1] + direction[pro[1]][1] * rest[persi]
        return x, y

    def move(self):
        global flag
        global current_po
        A = self.id - 1
        D = A ^ 1

        t = []

        # 攻防命令表，程序会按照顺序试图执行攻防命令，无法执行则读取下一条，可以执行则退出循环
        Mser = [
            [D, H, 0],
            [D, H, 1],
            [D, C, 0]
        ]
        print('----------------------------')
        print(Mser)
        for lssi in Mser:
            print(lssi)
            lsser = b[lssi[0]][lssi[1]][lssi[2]]
            lens = len(lsser)
            if lens > 0:
                t = random.randint(0, lens - 1)
                tli = lsser[t]
                break

        if t == []:
            x = random.randint(0, 14)
            y = random.randint(0, 14)
            while a[x][y] != 0:
                x = random.randint(0, 14)
                y = random.randint(0, 14)
            current_po = (x, y)

        else:
            print(tli)
            current_po = self.move_on(tli)

        flag = 1


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
        global flag
        flag = 2  # 只需要修改标志位为2，等待系统接收键盘点击事件即可


#####################
# 绘制棋子
# input: int x,y 落子在棋盘上的位置，int id 玩家Id，1 黑棋玩家；2 白棋玩家
# output: 无
#####################
def draw_piece(po, id):
    # 不进行合法性检查了
    x = po[0] * cellWidth + 10
    y = po[1] * cellWidth + 10
    if id == 1:
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
        return -1, -1

    # 根据点击位置计算落子位置
    tx = (mouse_x - 10) // cellWidth
    ty = (mouse_y - 10) // cellWidth

    # 判断当前位置上是否有棋子，有的话本次点击无效
    if a[tx][ty] != 0:
        return -1, -1

    return tx, ty


#####################
# 检测从一个点，到一个方向的棋型
# 输入：int x,y 棋盘上一个点位的坐标；dir 一个具体方向，定义在数组direction中
#####################

def q_type(x, y, dir_id):
    global b

    for player_id in (1, 2):  # 需要分开统计两名玩家各自的棋型库
        op_player_id = ((player_id - 1) ^ 1) + 1  # 非当前统计玩家的id
        q_type_value = 0  # 棋型的值
        q_ready = True  # 是否构成棋型，当连续的5个位置有对方棋子是不构成棋型
        huo_flag = False

        if a[x][y] == player_id:
            q_type_value += 1
        elif a[x][y] == op_player_id:  # 如果当前位置直接就是对手棋子则退出本次循环
            continue
        else:  # 如果当前位置为空位，则可以测活棋型，否则只能测冲棋型
            huo_flag = True

        q_dir = direction[dir_id]
        cx, cy = x, y
        for t in range(0, 4):  # 测试该方向接下来的四个位置
            cx = cx + q_dir[0]
            cy = cy + q_dir[1]

            if a[cx][cy] == op_player_id:  # 如果有对方的子，则
                q_ready = False
                break

            q_type_value = q_type_value << 1
            if a[cx][cy] == player_id:
                q_type_value += 1
        if not q_ready:  # 如果有对方子阻挡不构成棋型，则进行下一个循环
            continue

        if q_type_value == 0:  # 如果连续5个都为孔眼，则进行下一个循环
            continue

        # 测试活棋型,如果沿着这个方向下一个格子出界，或者不为空，则不能构成活棋型
        if huo_flag:
            if cx + q_dir[0] > 14 or cy + q_dir[1] > 14 or cy + q_dir[1] < 0:
                huo_flag = False
            elif a[cx + q_dir[0]][cy + q_dir[1]] != 0:
                huo_flag = False

        player_nu = player_id - 1
        if huo_flag:
            huo_nu = 0
        else:
            huo_nu = 1

        i = 0
        for q in qxmc:
            if q_type_value in q:
                b[player_nu][huo_nu][i].append(((x, y), dir_id, q_type_value))
            i += 1


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
    for i in range(LINES):
        a.append([])
        for j in range(LINES):
            a[i].append(0)  # 棋盘上每个格子初始为空

    # 初始化时钟
    clock = pygame.time.Clock()

    # 初始化玩家

    player1 = Human_player(1, 'kong')

    player2 = AI_rnd_player(2, 'haifeng')

    # 设置当前玩家为黑方
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
            # 重绘棋盘并刷新
            draw_piece(current_po, currentPlayer.id)
            pygame.display.update()

            a[current_po[0]][current_po[1]] = currentPlayer.id  # 将当前玩家落子存入数组

            # 获胜判定
            if judge_victory(current_po, currentPlayer.id):
                print(currentPlayer.name + "我赢了，哈哈哈哈哈哈啊哈哈！")

            # 记录棋型

            # 清空棋型库，重新计算全部棋型

            b = [[[[], [], [], []], [[], [], [], []]], [[[], [], [], []], [[], [], [], []]]]

            for vw in area:
                for x in range(vw[0][0], vw[0][1]):
                    for y in range(vw[1][0], vw[1][1]):
                        for d in vw[2]:
                            q_type(x, y, d)
            print('============================')
            print(b)
            # 转换玩家
            if currentPlayer == player1:
                currentPlayer = player2
            else:
                currentPlayer = player1

            # 当前玩家走子
            currentPlayer.move()

        time_passed = clock.tick(FPS)
