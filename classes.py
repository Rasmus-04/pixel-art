import pygame
from Config import *


pygame.init()
pygame.font.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pixlar Art")


class button:
    def __init__(self, txt=None, x=None, y=None, width=None, height=None, size=None, color=None, func=None, img=None, active=False, test_mode=False):
        self.txt = txt
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = size
        self.color = color
        self.func = func
        self.img = img
        self.active = False
        self.test_mode = test_mode

    def draw(self):
        if self.img == None:
            font = pygame.font.SysFont("comicsans", self.size)
            label = font.render(self.txt, 1, self.color)

            win.blit(label, (self.x, self.y))

            #draw_text(self.text, x=self.x, y=self.y, size=self.size, color=self.color)
            # Hit box
            if self.test_mode:
                pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height), 2)

        elif self.img != None:
            win.blit(self.img, (self.x, self.y))

            if self.test_mode:
                pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height), 2)


        self.check_klick()

    def check_klick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global run
                run = False
                pygame.display.quit()

        if self.img == None:
            # Check if cliked
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.x and pos[0] < (self.x + self.width):
                    if pos[1] > self.y and pos[1] < (self.y + self.height):
                        self.func()

        elif self.img != None:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.x and pos[0] < (self.x + self.width):
                    if pos[1] > self.y and pos[1] < (self.y + self.height):
                        time.sleep(0.1)
                        if not self.active:
                            self.active = True
                        else:
                            self.active = False



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
                pygame.display.quit()

        # Check if cliked
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if pos[0] > self.x and pos[0] < (self.x + self.size):
                if pos[1] > self.y and pos[1] < (self.y + self.size):
                    for i in all_color_buttons:
                        i.active_color = False

                    self.active_color = True
                    self.func(self.color)
