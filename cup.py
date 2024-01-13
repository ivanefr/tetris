import pygame
from constants import *


class Cup:
    def __init__(self, cup_x, cup_y, block, cup_width, cup_height):
        self.cup_width = cup_width
        self.cup_height = cup_height

        self.cup_x = cup_x
        self.cup_y = cup_y

        self.block = block

        self.lines = 0
        self.score = 0

        self.cup = self.get_new_cup_list()

    def get_new_cup_list(self):
        cup = []
        for i in range(self.cup_width):
            cup.append([' ' for _ in range(self.cup_height)])
        return cup

    def __getitem__(self, index):
        if isinstance(index, tuple):
            x, y = index
            return self.cup[x][y]
        else:
            return self.cup[index]

    def __setitem__(self, key, value):
        x, y = key
        self.cup[x][y] = value

    def draw(self, screen, color):
        pygame.draw.rect(screen, color,
                         (self.cup_x, self.cup_y,
                          self.cup_width * self.block,
                          self.cup_height * self.block,
                          ), 2)
        for x in range(self.cup_width):
            for y in range(self.cup_height):
                if self[x, y] != ' ':
                    pygame.draw.rect(screen, COLORS[int(self[x, y])],
                                     (self.cup_x + self.block * x,
                                      self.cup_y + self.block * y,
                                      self.block, self.block))
        for i in range(self.cup_height):
            if i < self.cup_width:
                pygame.draw.line(screen, WHITE,
                                 (self.cup_x + i * self.block, self.cup_y),
                                 (self.cup_x + i * self.block, self.cup_y + self.block * self.cup_height - 1), 1)
            pygame.draw.line(screen, WHITE,
                             (self.cup_x, self.cup_y + self.block * i),
                             (self.cup_x + self.cup_width * self.block - 1, self.cup_y + self.block * i), 1)

    def add_fig(self, fig):
        for x, y in fig.get_fig_coor:
            self[x, y] = fig.color
        c = 0
        for y in range(0, 20):
            for x in range(10):
                if self[x, y] == ' ':
                    break
            else:
                for x in range(10):
                    self[x].pop(y)
                    self[x].insert(0, ' ')
                c += 1
        self.update_score_by_lines(c)
        self.lines += c

    def check_pos(self, fig, deltax=0, deltay=0):
        fig_coor = fig.get_fig_coor
        for i in range(len(fig_coor)):
            fig_coor[i][0] += deltax
            fig_coor[i][1] += deltay
        for x, y in fig_coor:
            if x < 0 or x > self.cup_width - 1:
                return False
            if y < 0 or y > self.cup_height - 1:
                return False
            if self[x, y] != ' ':
                return False
        return True

    def clear(self):
        self.score = 0
        self.lines = 0
        self.cup = self.get_new_cup_list()

    def update_score_by_lines(self, count_lines):
        if count_lines == 1:
            self.score += 100
        elif count_lines == 2:
            self.score += 200
        elif count_lines == 3:
            self.score += 700
        elif count_lines == 4:
            self.score += 1500

    def update_score_by_falling(self, count_rotations, is_quick=False, height=None):
        if is_quick:
            if height >= 3:
                self.score += max(0, 3 * height - count_rotations * 2)
        else:
            self.score += max(0, 10 - count_rotations * 2)
