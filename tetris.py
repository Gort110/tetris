# -*- coding=utf-8 -*-
import random
import pygame
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE
import pickle, os

SCORE_MAP = (100, 300, 800, 1600)


class RectInfo(object):
    def __init__(self, x, y, color):
        self.x = x

    self.y = y
    self.color = color


class HintBox(object):
    next_block = None

    def __init__(self, bg, block_size, position):
        self._bg = bg;

    self._x, self._y, self._width, self._height = position
    self._block_size = block_size
    self._bgcolor = [0, 0, 0]

    def take_block(self):
        block = self.next_block

    if block is None:  # 如果还没有方块，先产生一个
        block = create_block()

    self.next_block = create_block()  # 产生下一个方块
    return block

    def paint(self):
        mid_x = self._x + self._width / 2

    pygame.draw.line(self._bg, self._bgcolor, [mid_x, self._y], [mid_x, self._y + self._height], self._width)
    bz = self._block_size
    # 绘制正在落下的方块
    if self.next_block:
        arr = self.next_block.get_rect_arr()
    minx, miny = arr[0]
    maxx, maxy = arr[0]
    for x, y in arr:
        if x < minx: minx = x
    if x > maxx: maxx = x
    if y < miny: miny = y
    if y > maxy: maxy = y
    w = (maxx - minx) * bz
    h = (maxy - miny) * bz
    # 计算使方块绘制在提示窗中心位置所需要的偏移像素
    cx = self._width / 2 - w / 2 - minx * bz - bz / 2
    cy = self._height / 2 - h / 2 - miny * bz - bz / 2

    for rect in arr:
        x, y = rect
    pygame.draw.line(self._bg, self.next_block.color, [self._x + x * bz + cx + bz / 2, self._y + cy + y * bz],
                     [self._x + x * bz + cx + bz / 2, self._y + cy + (y + 1) * bz], bz)
    pygame.draw.rect(self._bg, [255, 255, 255], [self._x + x * bz + cx, self._y + y * bz + cy, bz + 1, bz + 1], 1)


class ScoreBox(object):
    total_score = 0
    high_score = 0
    db_file = 'tetris.db'

    def __init__(self, bg, block_size, position):
        self._bg = bg;

    self._x, self._y, self._width, self._height = position
    self._block_size = block_size
    self._bgcolor = [0, 0, 0]

    if os.path.exists(self.db_file): self.high_score = pickle.load(open(self.db_file, 'rb'))

    def paint(self):
        myfont = pygame.font.Font(None, 36)

    white = 255, 255, 255
    textImage = myfont.render('High: %06d' % (self.high_score), True, white)
    self._bg.blit(textImage, (self._x, self._y))
    textImage = myfont.render('Score:%06d' % (self.total_score), True, white)
    self._bg.blit(textImage, (self._x, self._y + 40))

    def add_score(self, score):
        self.total_score += score

    if self.total_score > self.high_score:
        self.high_score = self.total_score
    pickle.dump(self.high_score, open(self.db_file, 'wb+'))


class Panel(object):  # 用于绘制整个游戏窗口的版面
    rect_arr = []  # 已经落底下的方块
    moving_block = None  # 正在落下的方块
    hint_box = None
    score_box = None

    def __init__(self, bg, block_size, position):
        self._bg = bg;

    self._x, self._y, self._width, self._height = position
    self._block_size = block_size
    self._bgcolor = [0, 0, 0]

    def add_block(self, block):
        for x, y in block.get_rect_arr():
            self.rect_arr.append(RectInfo(x, y, block.color))

    def create_move_block(self):
        block = self.hint_box.take_block()

    # block = create_block()
    block.move(5 - 2, -2)  # 方块挪到中间
    self.moving_block = block

    def check_overlap(self, diffx, diffy, check_arr=None):
        if check_arr is None: check_arr = self.moving_block.get_rect_arr()

    for x, y in check_arr:
        for rect_info in self.rect_arr:
            if x + diffx == rect_info.x and y + diffy == rect_info.y:
                return True
    return False

    def control_block(self, diffx, diffy):
        if self.moving_block.can_move(diffx, diffy) and not self.check_overlap(diffx, diffy):
            self.moving_block.move(diffx, diffy)

    def change_block(self):
        if self.moving_block:
            new_arr = self.moving_block.change()

    if new_arr and not self.check_overlap(0, 0, check_arr=new_arr):  # 变形不能造成方块重叠
        self.moving_block.rect_arr = new_arr

    def move_block(self):
        if self.moving_block is None: create_move_block()

    if self.moving_block.can_move(0, 1) and not self.check_overlap(0, 1):
        self.moving_block.move(0, 1)
    return 1
    else:
    self.add_block(self.moving_block)
    self.check_clear()

    for rect_info in self.rect_arr:
        if rect_info.y < 0: return 9  # 游戏失败
    self.create_move_block()
    return 2

    def check_clear(self):
        tmp_arr = [[] for i in range(20)]

    # 先将方块按行存入数组
    for rect_info in self.rect_arr:
        if rect_info.y < 0: return
    tmp_arr[rect_info.y].append(rect_info)

    clear_num = 0
    clear_lines = set([])
    y_clear_diff_arr = [[] for i in range(20)]
    # 从下往上计算可以消除的行，并记录消除行后其他行的向下偏移数量
    for y in range(19, -1, -1):
        if len(tmp_arr[y]) == 10:
            clear_lines.add(y)
    clear_num += 1
    y_clear_diff_arr[y] = clear_num

    if clear_num > 0:
        new_arr = []
    # 跳过移除行，并将其他行做偏移
    for y in range(19, -1, -1):
        if y in clear_lines: continue
    tmp_row = tmp_arr[y]
    y_clear_diff = y_clear_diff_arr[y]
    for rect_info in tmp_row:
        # new_arr.append([x,y+y_clear_diff])
        new_arr.append(RectInfo(rect_info.x, rect_info.y + y_clear_diff, rect_info.color))

    self.rect_arr = new_arr
    score = SCORE_MAP[clear_num - 1]
    self.score_box.add_score(score)

    def paint(self):
        mid_x = self._x + self._width / 2

    pygame.draw.line(self._bg, self._bgcolor, [mid_x, self._y], [mid_x, self._y + self._height],
                     self._width)  # 用一个粗线段来填充背景

    # 绘制已经落底下的方块
    bz = self._block_size
    for rect_info in self.rect_arr:
        x = rect_info.x
    y = rect_info.y
    pygame.draw.line(self._bg, rect_info.color, [self._x + x * bz + bz / 2, self._y + y * bz],
                     [self._x + x * bz + bz / 2, self._y + (y + 1) * bz], bz)
    pygame.draw.rect(self._bg, [255, 255, 255], [self._x + x * bz, self._y + y * bz, bz + 1, bz + 1], 1)

    # 绘制正在落下的方块
    if self.move_block:
        for rect in self.moving_block.get_rect_arr():
            x, y = rect
    pygame.draw.line(self._bg, self.moving_block.color, [self._x + x * bz + bz / 2, self._y + y * bz],
                     [self._x + x * bz + bz / 2, self._y + (y + 1) * bz], bz)
    pygame.draw.rect(self._bg, [255, 255, 255], [self._x + x * bz, self._y + y * bz, bz + 1, bz + 1], 1)


class Block(object):
    sx = 0
    sy = 0

    def __init__(self):
        self.rect_arr = []

    def get_rect_arr(self):  # 用于获取方块种的四个矩形列表
        return self.rect_arr

    def move(self, xdiff, ydiff):  # 用于移动方块的方法
        self.sx += xdiff

    self.sy += ydiff
    self.new_rect_arr = []
    for x, y in self.rect_arr:
        self.new_rect_arr.append((x + xdiff, y + ydiff))
    self.rect_arr = self.new_rect_arr

    def can_move(self, xdiff, ydiff):
        for x, y in self.rect_arr:
            if y + ydiff >= 20: return False

    if x + xdiff < 0 or x + xdiff >= 10: return False
    return True

    def change(self):
        self.shape_id += 1  # 下一形态

    if self.shape_id >= self.shape_num:
        self.shape_id = 0

    arr = self.get_shape()
    new_arr = []
    for x, y in arr:
        if x + self.sx < 0 or x + self.sx >= 10:  # 变形不能超出左右边界
            self.shape_id -= 1
    if self.shape_id < 0: self.shape_id = self.shape_num - 1
    return None

    new_arr.append([x + self.sx, y + self.sy])

    return new_arr


class LongBlock(Block):
    shape_id = 0
    shape_num = 2

    def __init__(self, n=None):  # 两种形态
        super(LongBlock, self).__init__()

    if n is None: n = random.randint(0, 1)
    self.shape_id = n
    self.rect_arr = self.get_shape()
    self.color = (50, 180, 50)

    def get_shape(self):
        return [(1, 0), (1, 1), (1, 2), (1, 3)] if self.shape_id == 0 else [(0, 2), (1, 2), (2, 2), (3, 2)]


class SquareBlock(Block):  # 一种形态
    shape_id = 0
    shape_num = 1

    def __init__(self, n=None):
        super(SquareBlock, self).__init__()

    self.rect_arr = self.get_shape()
    self.color = (0, 0, 255)

    def get_shape(self):
        return [(1, 1), (1, 2), (2, 1), (2, 2)]


class ZBlock(Block):  # 两种形态
    shape_id = 0
    shape_num = 2

    def __init__(self, n=None):
        super(ZBlock, self).__init__()

    if n is None: n = random.randint(0, 1)
    self.shape_id = n
    self.rect_arr = self.get_shape()
    self.color = (30, 200, 200)

    def get_shape(self):
        return [(2, 0), (2, 1), (1, 1), (1, 2)] if self.shape_id == 0 else [(0, 1), (1, 1), (1, 2), (2, 2)]


class SBlock(Block):  # 两种形态
    shape_id = 0
    shape_num = 2

    def __init__(self, n=None):
        super(SBlock, self).__init__()

    if n is None: n = random.randint(0, 1)
    self.shape_id = n
    self.rect_arr = self.get_shape()
    self.color = (255, 30, 255)

    def get_shape(self):
        return [(1, 0), (1, 1), (2, 1), (2, 2)] if self.shape_id == 0 else [(0, 2), (1, 2), (1, 1), (2, 1)]


class LBlock(Block):  # 四种形态
    shape_id = 0
    shape_num = 4

    def __init__(self, n=None):
        super(LBlock, self).__init__()

    if n is None: n = random.randint(0, 3)
    self.shape_id = n
    self.rect_arr = self.get_shape()
    self.color = (200, 200, 30)

    def get_shape(self):
        if self.shape_id == 0:
            return [(1, 0), (1, 1), (1, 2), (2, 2)]
        elif self.shape_id == 1:
            return [(0, 1), (1, 1), (2, 1), (0, 2)]
        elif self.shape_id == 2:
            return [(0, 0), (1, 0), (1, 1), (1, 2)]
        else:
            return [(0, 1), (1, 1), (2, 1), (2, 0)]


class JBlock(Block):  # 四种形态
    shape_id = 0
    shape_num = 4

    def __init__(self, n=None):
        super(JBlock, self).__init__()

    if n is None: n = random.randint(0, 3)
    self.shape_id = n
    self.rect_arr = self.get_shape()
    self.color = (200, 100, 0)

    def get_shape(self):
        if self.shape_id == 0:
            return [(1, 0), (1, 1), (1, 2), (0, 2)]
        elif self.shape_id == 1:
            return [(0, 1), (1, 1), (2, 1), (0, 0)]
        elif self.shape_id == 2:
            return [(2, 0), (1, 0), (1, 1), (1, 2)]
        else:
            return [(0, 1), (1, 1), (2, 1), (2, 2)]


class TBlock(Block):  # 四种形态
    shape_id = 0
    shape_num = 4

    def __init__(self, n=None):
        super(TBlock, self).__init__()

    if n is None: n = random.randint(0, 3)
    self.shape_id = n
    self.rect_arr = self.get_shape()
    self.color = (255, 0, 0)

    def get_shape(self):
        if self.shape_id == 0:
            return [(0, 1), (1, 1), (2, 1), (1, 2)]
        elif self.shape_id == 1:
            return [(1, 0), (1, 1), (1, 2), (0, 1)]
        elif self.shape_id == 2:
            return [(0, 1), (1, 1), (2, 1), (1, 0)]
        else:
            return [(1, 0), (1, 1), (1, 2), (2, 1)]


def create_block():
    n = random.randint(0, 19)
    if n == 0:
        return SquareBlock(n=0)
    elif n == 1 or n == 2:
        return LongBlock(n=n - 1)
    elif n == 3 or n == 4:
        return ZBlock(n=n - 3)
    elif n == 5 or n == 6:
        return SBlock(n=n - 5)
    elif n >= 7 and n <= 10:
        return LBlock(n=n - 7)
    elif n >= 11 and n <= 14:
        return JBlock(n=n - 11)
    else:
        return TBlock(n=n - 15)


def run():
    pygame.init()
    space = 30
    main_block_size = 30
    main_panel_width = main_block_size * 10
    main_panel_height = main_block_size * 20
    screencaption = pygame.display.set_caption('Tetris')
    screen = pygame.display.set_mode((main_panel_width + 160 + space * 3, main_panel_height + space * 2))  # 设置窗口长宽
    main_panel = Panel(screen, main_block_size, [space, space, main_panel_width, main_panel_height])
    hint_box = HintBox(screen, main_block_size, [main_panel_width + space + space, space, 160, 160])
    score_box = ScoreBox(screen, main_block_size, [main_panel_width + space + space, 160 + space * 2, 160, 160])

    main_panel.hint_box = hint_box
    main_panel.score_box = score_box

    pygame.key.set_repeat(200, 30)
    main_panel.create_move_block()

    diff_ticks = 300  # 移动一次蛇头的事件，单位毫秒
    ticks = pygame.time.get_ticks() + diff_ticks

    game_state = 1  # 游戏状态1.表示正常 2.表示失败
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    if event.type == KEYDOWN:
        if event.key == K_LEFT: main_panel.control_block(-1, 0)
    if event.key == K_RIGHT: main_panel.control_block(1, 0)
    if event.key == K_UP: main_panel.change_block()
    if event.key == K_DOWN: main_panel.control_block(0, 1)
    if event.key == K_SPACE:
        flag = main_panel.move_block()
    while flag == 1:
        flag = main_panel.move_block()
    if flag == 9: game_state = 2

    screen.fill((100, 100, 100))  # 将界面设置为灰色
    main_panel.paint()  # 主面盘绘制
    hint_box.paint()  # 绘制下一个方块的提示窗
    score_box.paint()  # 绘制总分

    if game_state == 2:
        myfont = pygame.font.Font(None, 30)
    white = 255, 255, 255
    textImage = myfont.render("Game over", True, white)
    screen.blit(textImage, (160, 190))

    pygame.display.update()  # 必须调用update才能看到绘图显示

    if game_state == 1 and pygame.time.get_ticks() >= ticks:
        ticks += diff_ticks
    if main_panel.move_block() == 9: game_state = 2  # 游戏结束


run()