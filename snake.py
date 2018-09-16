#!/usr/bin/python
# -*-coding: utf-8 -*-

import itertools
import pygame
import random
import sys
import time
from dataclasses import dataclass
from pygame.locals import *
from collections import deque
import operator

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARKGRAY = (40, 40, 40)


@dataclass
class Base:
    window_width: int = 320
    window_height: int = 320
    cell_size: int = 20

    cell_width = int(window_width / cell_size)
    cell_height = int(window_height / cell_size)


class Apple(Base):
    def __init__(self):
        self.location = None

    def refresh(self, snake):
        available_position = (
            set(itertools.product(range(self.cell_width - 1), range(self.cell_height - 1))) - set(snake.body)
        )
        try:
            location = random.sample(available_position, 1)[0]
        except ValueError:
            location = None
        self.location = location


class Snake(Base):
    def __init__(self, initial_length: int = 3):
        """
        :param initial_length: The initial length of the snake
        """
        self.initial_length = initial_length

        # TODO: start from the middle instead
        if not 0 < initial_length < self.cell_width:
            raise ValueError(f"Initial_length should fall in (0, {self.cell_width})")
        start_x = random.randint(initial_length + 2, self.cell_width - (initial_length + 3))
        start_y = random.randint(initial_length + 2, self.cell_height - (initial_length + 3))

        self.body = list(zip([start_x] * initial_length, range(start_y, start_y - initial_length, -1)))
        self.score = 0
        self.is_dead = False
        self.eaten = False

    def get_head(self):
        return self.body[-1]

    def cheak_dead(self):
        """
        Check if the snake is dead
        :return: Boolean
        """
        x, y = self.get_head()
        if not 0 <= x < self.cell_width or not 0 <= y < self.cell_height or (x, y) in self.body[:-1]:
            return True
        return False

    def cut_tail(self):
        self.body.pop(0)

    def move(self, new_head: tuple, apple: Apple):
        """
        Given the location of apple, decide if the apple is eaten (same location as the snake's head)
        :param new_head: (new_head_x, new_head_y)
        :param apple: Apple instance
        :return: Boolean. Whether the apple is eaten.
        """
        # make the move
        self.body.append(new_head)

        if self.cheak_dead():
            return

        # if the snake eats the apple, score adds 1
        if self.get_head() == apple.location:
            self.eaten = True
            self.score += 1
        # Otherwise, cut the tail so that snake moves forward without growing
        else:
            self.eaten = False
            self.cut_tail()


class Player(Base):
    def __init__(self, snake: Snake, apple: Apple):
        """
        :param snake: Snake instance
        :param apple: Apple instance
        """
        super().__init__()
        self.snake = snake
        self.apple = apple

    @staticmethod
    def _get_neighbours(node):
        """
        fetch and yield the four neighbours of a node
        :param node: (node_x, node_y)
        """
        for diff in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yield tuple(map(operator.add, node, diff))

    @staticmethod
    def is_node_in_queue(node, queue):
        """
        Check if element is in a nested list
        """
        return any(node in sublist for sublist in queue)

    def is_invalid_move(self, node: tuple, snake: Snake):
        """
        Similar to check_dead, this method checks if a given node is a valid move
        :return: Boolean
        """
        x, y = node
        if not 0 <= x < self.cell_width or not 0 <= y < self.cell_height or node in snake.body:
            return True
        return False


class BFS(Player):
    def __init__(self, snake: Snake, apple: Apple):
        """
        :param snake: Snake instance
        :param apple: Apple instance
        """
        super().__init__(snake=snake, apple=apple)

    def run(self):
        queue = deque([[self.snake.get_head()]])

        # TODO: if BFS has no way to go, return an elegant error
        while queue:
            path = queue.popleft()
            node = path[-1]

            # If snake eats the apple, return the next move after snake's head
            if node == self.apple.location:
                return path[1]

            for new_node in self._get_neighbours(node):
                if (
                    self.is_invalid_move(node=new_node, snake=self.snake)
                    or self.is_node_in_queue(node=new_node, queue=queue)
                ):
                    continue

                new_path = list(path)
                new_path.append(new_node)
                queue.append(new_path)


@dataclass
class SnakeGame(Base):
    fps: int = 60

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        self.basic_font = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Perfect Snake')

        self.cell_width = int(self.window_width / self.cell_size)
        self.cell_height = int(self.window_height / self.cell_size)

    def launch(self):
        while True:
            self.game()
            # self.showGameOverScreen()
            self.pause_game()

    def game(self):
        snake = Snake()

        apple = Apple()
        apple.refresh(snake=snake)

        while True:
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.terminate()

            bfs = BFS(snake=snake, apple=apple)
            # TODO: if BFS has no result, it should wonder
            snake.move(new_head=bfs.run(), apple=apple)

            if snake.is_dead:
                break
            elif snake.eaten:
                apple.refresh(snake=snake)

            self.display.fill(BLACK)
            self.draw_panel()
            self.draw_snake(snake.body)

            self.draw_apple(apple.location)
            pygame.display.update()
            self.clock.tick(self.fps)

        print(snake.score)

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    def pause_game(self):
        while True:
            time.sleep(0.2)
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    self.terminate()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    else:
                        return

    def draw_snake(self, snake_body):
        for snake_block_x, snake_block_y in snake_body:
            x = snake_block_x * self.cell_size
            y = snake_block_y * self.cell_size
            snake_block = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.display, WHITE, snake_block)

    def draw_apple(self, apple_location):
        apple_x, apple_y = apple_location
        apple_block = pygame.Rect(apple_x * self.cell_size, apple_y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.display, RED, apple_block)

    def draw_panel(self):
        for x in range(0, self.window_width, self.cell_size):  # draw vertical lines
            pygame.draw.line(self.display, DARKGRAY, (x, 0), (x, self.window_height))
        for y in range(0, self.window_height, self.cell_size):  # draw horizontal lines
            pygame.draw.line(self.display, DARKGRAY, (0, y), (self.window_width, y))


if __name__ == '__main__':
    SnakeGame().launch()
