from snake import *


snake = Snake(body=[(0,0),(0,1),(0,2)])
apple = Apple()
apple.location=(8,8)


one = StepLongestPath(snake=snake, apple=apple)

