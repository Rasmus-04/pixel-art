from random import randint
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (4, 51, 255)
GREEN = (0, 255, 0)
GRAY = (128,128,128)

WIDTH, HEIGHT = 800, 800
canvisX, canvisY, = 600, 600
canvisX_start, canvisY_start = (WIDTH - canvisX)/2, (HEIGHT - canvisY)/2 - 50
block_size = 15
timer = 0
active_color = (randint(0,255), randint(0,255),randint(0,255))

block_start_color = (255,255,255)

blocks = []
all_color_buttons = []

run = True
enter_settings = False