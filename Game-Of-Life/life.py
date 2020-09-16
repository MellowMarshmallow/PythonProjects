#!/usr/bin/env python3


import pygame
import random


class Cells:

    def __init__(self, rows, columns):
        self.m = rows
        self.n = columns
        self.board = [[0] * columns for _ in range(rows)]

    def _update_cell(self, r, c):
        neighbour = 0
        for i in range(max(0, r - 1), min(r + 2, self.m)):
            for j in range(max(0, c - 1), min(c + 2, self.n)):
                neighbour += self.board[i][j] & 1
        if neighbour == 3 or neighbour == self.board[r][c] + 3:
            self.board[r][c] += 2

    def update_board(self):
        for i in range(self.m):
            for j in range(self.n):
                self._update_cell(i, j)
        for k in range(self.m):
            for l in range(self.n):
                self.board[k][l] >>= 1

    def set_new_board(self, board):
        self.board = board
        self.m = len(board)
        self.n = len(board[0])

    def randomize_board(self):
        for i in range(self.m):
            for j in range(self.n):
                self.board[i][j] = random.randint(0, 1)

    def draw_board(self, surface, w, h):
        cell_w = w / self.n
        cell_h = h / self.m
        for i in range(self.m):
            for j in range(self.n):
                cell = pygame.Rect(i * cell_w, j * cell_h, cell_w, cell_h)
                colour = (187, 194, 207) if self.board[i][j] else (40, 44, 52)
                pygame.draw.rect(surface, colour, cell)


def main():
    WIDTH = 600
    HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    life = Cells(60, 60)
    life.randomize_board()

    running = True
    fps = 12

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    life.randomize_board()
                elif event.key == pygame.K_j and fps > 4:
                    fps -= 4
                elif event.key == pygame.K_k and fps < 56:
                    fps += 4

        life.update_board()
        life.draw_board(screen, WIDTH, HEIGHT)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()
