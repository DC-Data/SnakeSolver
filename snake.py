#!/usr/bin/python
# -*-coding: utf-8 -*-

import pygame
from pygame.locals import *
import random
import sys
import time
from operator import add, sub
from dataclasses import dataclass
from itertools import product
from collections import deque
from typing import Tuple

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGRAY = (40, 40, 40)


@dataclass
class Base:
    cell_size: int = 20
    cell_width: int = 16
    cell_height: int = 16
    window_width = cell_size * cell_width
    window_height = cell_size * cell_height

    @staticmethod
    def node_add(node_a: Tuple[int, int], node_b: Tuple[int, int]):
        result: Tuple[int, int] = tuple(map(add, node_a, node_b))
        return result

    @staticmethod
    def node_sub(node_a: Tuple[int, int], node_b: Tuple[int, int]):
        result: Tuple[int, int] = tuple(map(sub, node_a, node_b))
        return result


class Apple(Base):
    def __init__(self):
        self.location = None

    def refresh(self, snake):
        """
        Generate a new apple
        """
        available_positions = set(product(range(self.cell_width - 1), range(self.cell_height - 1))) - set(snake.body)
        if available_positions:
            location = random.sample(available_positions, 1)[0]
        # If there's no available node for new apple, it reaches the perfect solution. Don't draw the apple then.
        else:
            location = (-1, -1)
        self.location = location


class Snake(Base):
    def __init__(self, initial_length: int = 3):
        """
        :param initial_length: The initial length of the snake
        """
        self.initial_length = initial_length

        if not 0 < initial_length < self.cell_width:
            raise ValueError(f"Initial_length should fall in (0, {self.cell_width})")

        start_x = self.cell_width // 2
        start_y = self.cell_height // 2

        start_body_x = [start_x] * initial_length
        start_body_y = range(start_y, start_y - initial_length, -1)

        self.body = deque(zip(start_body_x, start_body_y))
        self.score = 0
        self.is_dead = False
        self.eaten = False

        # last_direction is only used for human player, giving it a default direction when game starts
        self.last_direction = (-1, 0)

    def get_head(self):
        return self.body[-1]

    def cheak_dead(self, new_head):
        """
        Check if the snake is dead
        :return: Boolean
        """
        x, y = new_head
        if not 0 <= x < self.cell_width or not 0 <= y < self.cell_height or new_head in self.body:
            self.is_dead = True
            return True
        return False

    def cut_tail(self):
        self.body.popleft()

    def move(self, new_head: tuple, apple: Apple):
        """
        Given the location of apple, decide if the apple is eaten (same location as the snake's head)
        :param new_head: (new_head_x, new_head_y)
        :param apple: Apple instance
        :return: Boolean. Whether the apple is eaten.
        """
        if new_head is None:
            self.is_dead = True
            return

        if self.cheak_dead(new_head=new_head):
            return

        self.last_direction = self.node_sub(new_head, self.get_head())

        # make the move
        self.body.append(new_head)

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

    def _get_neighbors(self, node):
        """
        fetch and yield the four neighbours of a node
        :param node: (node_x, node_y)
        """
        for diff in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            yield self.node_add(node, diff)

    @staticmethod
    def is_node_in_queue(node: tuple, queue: iter):
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
        """
        Run BFS searching and return the full path of best way to apple from BFS searching
        """
        queue = deque([deque([self.snake.get_head()])])

        while queue:
            path = queue[0]
            future_head = path[-1]

            # If snake eats the apple, return the next move after snake's head
            if future_head == self.apple.location:
                return path

            for next_node in self._get_neighbors(future_head):
                if (
                    self.is_invalid_move(node=next_node, snake=self.snake)
                    or self.is_node_in_queue(node=next_node, queue=queue)
                ):
                    continue
                new_path = deque(path)
                new_path.append(next_node)
                queue.append(new_path)

            queue.popleft()

    def next_node(self):
        """
        Run the BFS searching and return the next move in this path
        """
        path = self.run()
        return path[1]


class HamiltonianPath(Player):
    def __init__(self, snake: Snake, apple: Apple):
        """
        :param snake: Snake instance
        :param apple: Apple instance
        """
        super().__init__(snake=snake, apple=apple)


class Human(Player):
    def __init__(self, snake: Snake, apple: Apple):
        """
        :param snake: Snake instance
        :param apple: Apple instance
        """
        super().__init__(snake=snake, apple=apple)

    def run(self):
        for event in pygame.event.get():  # event handling loop
            if event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and self.snake.last_direction != (1, 0):
                    diff = (-1, 0)  # left
                elif (event.key == K_RIGHT or event.key == K_d) and self.snake.last_direction != (-1, 0):
                    diff = (1, 0)  # right
                elif (event.key == K_UP or event.key == K_w) and self.snake.last_direction != (0, 1):
                    diff = (0, -1)  # up
                elif (event.key == K_DOWN or event.key == K_s) and self.snake.last_direction != (0, -1):
                    diff = (0, 1)  # down
                else:
                    break
                return self.node_add(self.snake.get_head(), diff)
        # If no button is pressed down, follow previou direction
        return self.node_add(self.snake.get_head(), self.snake.last_direction)


@dataclass
class SnakeGame(Base):
    fps: int = 90

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        self.basic_font = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Perfect Snake')

    def launch(self):
        while True:
            self.game()
            # self.showGameOverScreen()
            self.pause_game()

    def game(self):
        snake = Snake()

        apple = Apple()
        apple.refresh(snake=snake)

        step_time = []

        while True:
            # Human Player
            # new_head = Human(snake=snake, apple=apple).run()

            # AI Player
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.terminate()

            start_time = time.time()
            new_head = BFS(snake=snake, apple=apple).next_node()
            end_time = time.time()
            step_time.append(end_time - start_time)

            snake.move(new_head=new_head, apple=apple)

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

        print(f"Score: {snake.score}")
        print(f"Mean step time: {round(sum(step_time)/len(step_time), 4)}")

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
            snake_block = pygame.Rect(x, y, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(self.display, WHITE, snake_block)

        # Draw snake's head
        x = snake_body[-1][0] * self.cell_size
        y = snake_body[-1][1] * self.cell_size
        snake_block = pygame.Rect(x, y, self.cell_size - 1, self.cell_size - 1)
        pygame.draw.rect(self.display, GREEN, snake_block)

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
