import pygame
from Config import *
import time


pygame.init()
pygame.font.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pixlar Art")

class button:
    def __init__(self, text, x, y, width, height, size, color, func, test_mode=False):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = size
        self.color = color
        self.func = func
        self.test_mode = test_mode

    def draw(self):
        draw_text(self.text, x=self.x, y=self.y, size=self.size, color=self.color)
        # Hit box
        if self.test_mode:
            pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height), 2)

        self.check_klick()

    def check_klick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global run
                run = False

        # Check if cliked
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if pos[0] > self.x and pos[0] < (self.x + self.width):
                if pos[1] > self.y and pos[1] < (self.y + self.height):
                    self.func()


class colors_button:
    def __init__(self, color, x, y, func=None, size=50):
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.func = func
        self.active_color = False

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

        self.check_klick()

    def check_klick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global run
                run = False

        # Check if cliked
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if pos[0] > self.x and pos[0] < (self.x + self.size):
                if pos[1] > self.y and pos[1] < (self.y + self.size):
                    for i in all_color_buttons:
                        i.active_color = False

                    self.active_color = True
                    self.func(self.color)





def draw_text(txt, x=0, y=0, middleX=False, middleY=False, color=(0,0,0), font="comicsans", size=30, bold=False, italic=False):
    font = pygame.font.SysFont(font, size, bold=bold, italic=italic)
    label = font.render(txt, 1, color)

    if middleX:
        x = WIDTH/2 - label.get_width()/2

    if middleY:
        y = HEIGHT/2 - label.get_height()/2

    win.blit(label, (x,y))


def clear_canvis():
    for i in blocks:
        i[1] = block_start_color


def get_block_pos():
    for i in range(int(canvisX/block_size)):
        for j in range(int(canvisY/block_size)):
            blocks.append([(canvisX_start + i * block_size, canvisY_start + j * block_size), block_start_color])


def draw_grid():
    for i in range(int(canvisX/block_size) + 1):
        pygame.draw.line(win, GRAY, (canvisX_start + block_size * i, canvisY_start), (canvisX_start + block_size * i, canvisY_start + canvisY), 1)
        #pygame.draw.circle(win, GREEN, (canvisX_start + block_size * i, canvisY_start), 5)

    for i in range(int(canvisY/block_size) + 1):
        pygame.draw.line(win, GRAY, (canvisX_start, canvisY_start + block_size * i), (canvisX + canvisX_start, canvisY_start + block_size * i), 1)
        #pygame.draw.circle(win, GREEN, (canvisX_start, canvisY_start + i*block_size), 5)


def draw_blocks():
    for i in blocks:
        pos = i[0]
        color = i[1]
        pygame.draw.rect(win, color, (pos[0], pos[1], block_size, block_size))


def draw_canvis():
    #Black border around the canvis
    pygame.draw.rect(win, (BLACK), (canvisX_start, canvisY_start, canvisX, canvisY), 5)

    draw_blocks()
    draw_grid()


def draw(pos, color):
    for i in blocks:
        block_pos = i[0]
        if pos[0] > block_pos[0] and pos[0] < (block_pos[0] + block_size):
            if pos[1] > block_pos[1] and pos[1] < (block_pos[1] + block_size):
                i[1] = color


def change_active_color(color):
    global active_color
    active_color_button.color = color
    active_color = color


def save():
    with open("Last_painting.txt", "w") as f:
        for i in blocks:
            f.write(str(i[1][0]) + " ")
            f.write(str(i[1][1]) + " ")
            f.write(str(i[1][2]) + "\n")


def load():
    colors = []
    with open("Last_painting.txt", "r") as f:
        f = f.readlines()

    for index, i in enumerate(f):
        i = i.split(" ")
        blocks[index][1] = (int(i[0]), int(i[1]), int(i[2]))


def redraw_win():
    win.fill(WHITE)
    draw_canvis()

    reset_button.draw()
    save_button.draw()
    load_button.draw()

    draw_text("Pixlar Art", middleX=True, size=60)

    draw_text("Active Color", x=active_color_button.x - 30, y=active_color_button.y - 20, color=active_color)

    for color_button in all_color_buttons:
        color_button.draw()

    pygame.display.update()


reset_button = button("Clear", 30, HEIGHT- 100, 94, 34, 50, BLACK, clear_canvis)
save_button = button("Save", WIDTH/2 - 100, HEIGHT - 100, 85, 34, 50, BLACK, save)
load_button = button("Load", WIDTH/2, HEIGHT - 100, 85, 34, 50, BLACK, load)


active_color_button = colors_button(active_color, WIDTH - 100, HEIGHT - 90)
all_color_buttons.append(active_color_button)
black_color_button = colors_button(BLACK, WIDTH - 75, canvisY_start + 55, change_active_color)
all_color_buttons.append(black_color_button)
random_color_button = colors_button(BLACK, black_color_button.x, black_color_button.y - 55, change_active_color)
all_color_buttons.append(random_color_button)
red_color_button = colors_button(RED, random_color_button.x, black_color_button.y + 55, change_active_color)
all_color_buttons.append(red_color_button)
green_color_button = colors_button(GREEN, random_color_button.x, red_color_button.y + 55, change_active_color)
all_color_buttons.append(green_color_button)
blue_color_button = colors_button(BLUE, random_color_button.x, green_color_button.y + 55, change_active_color)
all_color_buttons.append(blue_color_button)
gray_color_button = colors_button(GRAY, random_color_button.x, blue_color_button.y + 55, change_active_color)
all_color_buttons.append(gray_color_button)
rainbow_color_button = colors_button(BLACK, random_color_button.x, gray_color_button.y + 55, change_active_color)
all_color_buttons.append(rainbow_color_button)




get_block_pos()
while run:
    redraw_win()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if pygame.mouse.get_pressed()[0]:
        draw(pygame.mouse.get_pos(), active_color)
    else:
        if pygame.mouse.get_pressed()[2]:
            draw(pygame.mouse.get_pos(), block_start_color)


    if timer <= 0:
        random_color_button.color = (randint(0,255), randint(0,255), randint(0,255))
        timer = 50
    elif timer % 10 == 0:
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        rainbow_color_button.color = color
        if rainbow_color_button.active_color:
            active_color = color
            active_color_button.color = color
        timer -= 1
    else:
        timer -= 1


pygame.display.quit()
