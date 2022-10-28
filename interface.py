import random
import time

import pygame

from robots.greedy_robot import GreedyRobot
from robots.role_robot import RoleRobot

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)


class Interface:
    def __init__(self, grid):
        self.grid = grid

        # load images
        self.greedy_robot = pygame.image.load("img/greedy_robot.png")
        self.random_robot = pygame.image.load("img/random_robot.png")
        self.obstacle = pygame.image.load("img/obstacle.png")
        self.trash = pygame.image.load("img/trash.png")
        self.plastic_bottle = pygame.image.load("img/plastic_bottle.png")
        self.bg = pygame.image.load("img/grass.jpeg")

        self.trash_img = {}

        pygame.init()

        # Open a new window
        self.line, self.column = grid.get_size()
        self.block_size = 70
        self.width, self.height = self.column * \
            self.block_size, self.line * self.block_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Multi Agent System")

    def draw_robot(self, pos, robot):
        if isinstance(robot, GreedyRobot) or isinstance(robot, RoleRobot):
            self.screen.blit(self.greedy_robot, pos)
        else:
            self.screen.blit(self.random_robot, pos)

    def draw_obstacle(self, pos):
        self.screen.blit(self.obstacle, pos)

    def draw_trash(self, pos):
        if pos not in self.trash_img:
            self.trash_img[pos] = random.choice(
                [self.trash, self.plastic_bottle])
        self.screen.blit(self.trash_img[pos], pos)

    def draw_bg(self):
        self.screen.fill(GREEN)

    def draw_grid(self):
        for pos in self.grid.get_trash():
            pos = (pos[1] * self.block_size,
                   pos[0] * self.block_size)
            self.draw_trash(pos)

        for pos in self.grid.get_obstacles():
            pos = (pos[1] * self.block_size,
                   pos[0] * self.block_size)
            self.draw_obstacle(pos)

        for robot in self.grid.get_robots():
            pos = robot.get_position()
            pos = (pos[1] * self.block_size,
                   pos[0] * self.block_size)
            self.draw_robot(pos, robot)

        for x in range(0, self.width, self.block_size):
            for y in range(0, self.height, self.block_size):
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    def render(self):

        wait_time = 0.5

        start = time.time()

        self.draw_bg()
        self.draw_grid()

        sleep_time = wait_time - (time.time() - start)
        if sleep_time > 0:
            time.sleep(sleep_time)
        pygame.display.update()

    def game_loop(self):
        # game loop
        start = time.time()

        self.draw_bg()
        self.draw_grid()
        pygame.display.update()

        wait_time = 0.5

        while len(self.grid.get_trash()) != 0:
            start = time.time()

            self.draw_bg()
            self.draw_grid()
            self.grid.step()

            sleep_time = wait_time - (time.time() - start)
            if sleep_time > 0:
                time.sleep(sleep_time)
            pygame.display.update()

        start = time.time()
        self.draw_bg()
        self.draw_grid()
        sleep_time = wait_time - (time.time() - start)
        if sleep_time > 0:
            time.sleep(sleep_time)
        pygame.display.update()
        time.sleep(1)
