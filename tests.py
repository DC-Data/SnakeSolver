from snake import *


snake = Snake(body=[(0,0),(0,1),(0,2)])
apple = Apple()
apple.location=(8,8)
l=LongestPath(snake=snake, apple=apple)
# add_result = l.node_add((1,1), (2,2))
# print(add_result)
SnakeGame().draw_snake(l.run())
