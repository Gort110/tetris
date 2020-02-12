# -*-coding:utf-8-*-
import random
import pygame
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN

class Panel(object):
    rect_arr = []
    moving_block = None
    def __init__(self, bg, block_size, position):
        self._bg = bg
        self._x, self._y, self._width, self._height = position
        self._block_size = block_size
        self._bgcolor = [0, 0, 0]
    def paint(self):
        mid_x = self._x + self._width/2
        pygame.draw.line(self._bg, self._bgcolor, [mid_x, self._y], [mid_x, self._y+self._height], self._width)
        bz = self._block_size
        for rect in self.rect_arr:
            x, y = rect
            pygame.draw.line(self._bg, [0, 0, 255], [self._x + x * bz + bz / 2, self._y + y * bz],
                             [self._x + x * bz + bz / 2, self._y + (y + 1) * bz], bz)
            pygame.draw.rect(self._bg, [255, 255, 255], [self._x + x * bz, self._y + y * bz, bz, bz], 1)
        if self.move_block:
            for rect in self.moving_block.get_rect_arr():
                x, y = rect
                pygame.draw.line(self._bg, [0, 0, 255], [self._x + x * bz + bz / 2, self._y + y * bz],
                                 [self._x + x * bz + bz / 2, self._y + (y + 1) * bz], bz)
                pygame.draw.rect(self._bg, [255, 255, 255], [self._x + x * bz, self._y + y * bz, bz, bz], 1)
    def add_block(self,block):
        for rect in block.get_rect_arr():
            self.rect_arr.append(rect)
    def check_overlap(self, diffx, diffy):
        for x, y in self.moving_block.get_rect_arr():
            for rx, ry in self.rect_arr:
                if x+diffx == rx and y+diffy == ry:
                    return True
        return False
    def create_move_block(self):
        block = create_block()
        block.move(3, -2)
        self.moving_block = block
    def move_block(self):
        if self.moving_block is None:
            self.create_move_block()
        if self.moving_block.can_move(0, 1) and not self.check_overlap(0,1):
            self.moving_block.move(0, 1)
        else:
            self.add_block(self.moving_block)
            self.create_move_block()
    def control_block(self, diffx, diffy):
        if self.moving_block.can_move(diffx, diffy) and not self.check_overlap(diffx, diffy):
            self.moving_block.move(diffx, diffy)

#Block define
class Block(object):
    def __init__(self):
        self.rect_arr = []
    def get_rect_arr(self):
        return self.rect_arr
    def move(self, xdiff, ydiff):
        self.new_rect_arr = []
        for x, y in self.rect_arr:
            self.new_rect_arr.append((x+xdiff, y+ydiff))
        self.rect_arr = self.new_rect_arr
    def can_move(self, xdiff, ydiff):
        for x, y in self.rect_arr:
            if y + ydiff >= 20:
                return False
            if x+xdiff < 0 or x+xdiff >= 10:
                return False
        return True
class LongBlock(Block):
    def __init__(self, n=None):
        super().__init__()
        if n is None:
            n = random.randint(0, 1)
        if n == 0:
            self.rect_arr = [(1, 0), (1, 1), (1, 2), (1, 3)]
        else:
            self.rect_arr = [(0, 2), (1, 2), (2, 2), (3, 2)]
class SquareBlock(Block):
    def __init__(self, n=None):
        super().__init__()
        self.rect_arr = [(1, 1), (1, 2), (2, 1), (2, 2)]

class ZBlock(Block):
    def __init__(self, n=None):
        super().__init__()
        if n is None:
            n = random.randint(0, 1)
        if n == 0:
            self.rect_arr = [(2, 0), (2, 1), (1, 1), (1, 2)]
        else:
            self.rect_arr = [(0, 1), (1, 1), (1, 2), (2, 2)]
class SBlock(Block):
    def __init__(self, n=None):
        super().__init__()
        if n is None:
            n = random.randint(0, 1)
        if n == 0:
            self.rect_arr = [(1, 0), (1, 1), (2, 1), (2, 2)]
        else:
            self.rect_arr = [(0, 2), (1, 2), (1, 1), (2, 1)]
class LBlock(Block):
    def __init__(self, n=None):
        super().__init__()
        if n is None:
            n = random.randint(0, 3)
        if n == 0:
            self.rect_arr = [(1, 0), (1, 1), (1, 2), (2, 2)]
        elif n == 1:
            self.rect_arr = [(0, 1), (1, 1), (2, 1), (0, 2)]
        elif n == 2:
            self.rect_arr = [(0, 0), (1, 0), (1, 1), (1, 2)]
        else:
            self.rect_arr = [(0, 1), (1, 1), (2, 1), (2, 0)]
class JBlock(Block):
    def __init__(self, n=None):
        super().__init__()
        if n is None:
            n = random.randint(0, 3)
        if n == 0:
            self.rect_arr = [(1, 0), (1, 1), (1, 2), (0, 2)]
        elif n == 1:
            self.rect_arr = [(0, 1), (1, 1), (2, 1), (0, 0)]
        elif n == 2:
            self.rect_arr = [(2, 0), (1, 0), (1, 1), (1, 2)]
        else:
            self.rect_arr = [(0, 1), (1, 1), (2, 1), (2, 2)]
class LBlock(Block):
    def __init__(self, n=None):
        super().__init__()
        if n is None:
            n = random.randint(0, 3)
        if n == 0:
            self.rect_arr = [(1, 0), (1, 1), (1, 2), (2, 2)]
        elif n == 1:
            self.rect_arr = [(0, 1), (1, 1), (2, 1), (0, 2)]
        elif n == 2:
            self.rect_arr = [(0, 0), (1, 0), (1, 1), (1, 2)]
        else:
            self.rect_arr = [(0, 1), (1, 1), (2, 1), (2, 0)]
class TBlock(Block):
    def __init__(self, n=None):
        super().__init__()
        if n is None:
            n = random.randint(0, 3)
        if n == 0:
            self.rect_arr = [(0, 1), (1, 1), (2, 1), (1, 2)]
        elif n == 1:
            self.rect_arr = [(1, 0), (1, 1), (1, 2), (0, 1)]
        elif n == 2:
            self.rect_arr = [(0, 1), (1, 1), (2, 1), (1, 0)]
        else:
            self.rect_arr = [(1, 0), (1, 1), (1, 2), (2, 1)]

def create_block():
    n = random.randint(0, 19)
    if n == 0:
        return SquareBlock(n=0)
    elif n == 1 or n == 2:
        return LongBlock(n=n-1)
    elif n == 3 or n == 4:
        return ZBlock(n=n-3)
    elif n == 5 or n == 6:
        return SBlock(n=n-5)
    elif 7 <= n <= 10:
        return LongBlock(n=n-7)
    elif 11 <= n <= 14:
        return LongBlock(n=n-11)
    else:
        return TBlock(n=n-15)


def run():
    pygame.init()
    space = 30
    main_block_size = 30
    main_panel_width = main_block_size * 10
    main_panel_height = main_block_size * 20
    pygame.display.set_caption("Tetris")
    screen = pygame.display.set_mode((main_panel_width+160+space*3, main_panel_height+space*2))
    main_panel = Panel(screen, main_block_size,[space, space, main_panel_width, main_panel_height])

    pygame.key.set_repeat(200, 30)
    main_panel.create_move_block()
    diff_ticks = 300  # 移动一次蛇头的事件，单位毫秒
    ticks = pygame.time.get_ticks() + diff_ticks

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    main_panel.control_block(-1, 0)
                if event.key == K_RIGHT:
                    main_panel.control_block(1, 0)
                if event.key == K_UP:
                    pass  # 变形过会实现
                if event.key == K_DOWN:
                    main_panel.control_block(0, 1)
        screen.fill((100, 100, 100))
        main_panel.paint()
        pygame.display.update()
        if pygame.time.get_ticks() >= ticks:
            ticks = ticks + diff_ticks
            main_panel.move_block()




run()