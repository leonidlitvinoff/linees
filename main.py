import pygame
from board import Board
import copy
class Life(Board):
    def __init__(self, width, height, rect, pos, width_w=500, height_w=500):
        super().__init__(width, height, rect, pos)
        self.width_w = width_w
        self.height_w = height_w
        self.screen = pygame.display.set_mode((self.width_w, self.height_w))
        self.red_count = 0
        self.count = 0
        self.itog = False
        self.run()

    def render(self, screen):
        screen.fill((0, 0, 0))
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (i * self.rect[0] + self.pos[0], j * self.rect[1] + self.pos[1],
                                                               self.rect[0], self.rect[1]), 1)
                elif self.board[i][j] == 1:
                    pygame.draw.ellipse(screen, (0, 0, 255),
                                     (i * self.rect[0] + self.pos[0], j * self.rect[1] + self.pos[1],
                                      self.rect[0], self.rect[1]), 0)
                elif self.board[i][j] == 2:
                    pygame.draw.ellipse(screen, (255, 0, 0),
                                     (i * self.rect[0] + self.pos[0], j * self.rect[1] + self.pos[1],
                                      self.rect[0], self.rect[1]), 0)


    def has_path(self, x1, y1, x2, y2):
        self.need = (x2, y2)
        self.count = 0
        self.itog = False
        self.board2 = [i for i in self.board]
        self.bfs(x1, y1)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 4:
                    self.board[i][j] = 0
        return self.itog

    def bfs(self, x, y):
        if self.board2[y][x] == 2:
            self.count += 1
        if self.count == 2:
            self.itog = True
            return
        self.board2[y][x] = 4
        if self.check(x - 1, y):
            if self.board2[y][x - 1] != 1 and self.board2[y][x - 1] != 4:
                self.bfs(x - 1, y)
        if self.check(x + 1, y):
            if self.board2[y][x + 1] != 1 and self.board2[y][x + 1] != 4:
                self.bfs(x + 1, y)
        if self.check(x - 1, y - 1):
            if self.board2[y - 1][x - 1] != 1 and self.board2[y - 1][x - 1] != 4:
                self.bfs(x - 1, y - 1)
        if self.check(x, y - 1):
            if self.board2[y - 1][x] != 1 and self.board2[y - 1][x] != 4:
                self.bfs(x, y - 1)
        if self.check(x + 1, y - 1):
            if self.board2[y - 1][x + 1] != 1 and self.board2[y - 1][x + 1] != 4:
                self.bfs(x + 1, y - 1)
        if self.check(x + 1, y + 1):
            if self.board2[y + 1][x + 1] != 1 and self.board2[y + 1][x + 1] != 4:
                self.bfs(x + 1, y + 1)
        if self.check(x, y + 1):
            if self.board2[y + 1][x] != 1 and self.board2[y + 1][x] != 4:
                self.bfs(x, y + 1)
        if self.check(x - 1, y + 1):
            if self.board2[y + 1][x - 1] != 1 and self.board2[y + 1][x - 1] != 4:
                self.bfs(x - 1, y + 1)

    def check(self, x, y):
        if x < 0 or y < 0:
            return False
        try:
            a = self.board[y][x]
            return True
        except:
            return False

    def run(self):
        pygame.init()
        running = True
        self.screen.fill((0, 0, 0))
        fps = 60
        clock = pygame.time.Clock()
        last_mouse_left_click = 0
        while running:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if pygame.mouse.get_pressed()[0]:
                last_mouse_left_click = 1
            else:
                if last_mouse_left_click:
                    last_mouse_left_click = 0
                    coords = self.get_cell(pygame.mouse.get_pos())
                    if self.board[coords[0]][coords[1]] == 0:
                        if not self.red_count == 1:
                            self.board[coords[0]][coords[1]] = 1
                        else:
                            coords2 = (0, 0)
                            for i in range(len(self.board)):
                                for j in range(len(self.board[i])):
                                    if self.board[i][j] == 2:
                                        coords2 = (j, i)
                                        break
                            self.board[coords[0]][coords[1]] = 2
                            m = self.has_path(coords[0], coords[1], coords2[0], coords2[1])
                            if m:
                                self.board[coords2[0]][coords2[1]] = 0
                                self.board[coords[0]][coords[1]] = 1
                                self.red_count -= 1
                    elif self.board[coords[0]][coords[1]] == 1:
                        self.red_count += 1
                        self.board[coords[0]][coords[1]] = 2
                    elif self.board[coords[0]][coords[1]] == 2:
                        self.board[coords[0]][coords[1]] = 1
                        self.red_count -= 1
            self.render(self.screen)
            pygame.display.flip()
Life(10, 10, (50, 50), (0, 0))