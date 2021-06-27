import time
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
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
                settings_button.active = False

        if self.img == None:
            # Check if cliked
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.x and pos[0] < (self.x + self.width):
                    if pos[1] > self.y and pos[1] < (self.y + self.height):
                        self.func()
                        if self.test_mode:
                            print("Works")

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
                        if self.func != None:
                            self.func()
                        if self.test_mode:
                            print("Works")



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
                settings_button.active = False

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
    # Black border around the canvis
    pygame.draw.rect(win, (BLACK), (canvisX_start, canvisY_start, canvisX, canvisY), 5)
    draw_blocks()
    if draw_grid_on_canvis:
        draw_grid()


def draw(pos, color):
    for i in blocks:
        block_pos = i[0]
        if pos[0] > block_pos[0] and pos[0] < (block_pos[0] + block_size):
            if pos[1] > block_pos[1] and pos[1] < (block_pos[1] + block_size):
                i[1] = color


def get_color_from_canvis(pos):
    global active_color
    for i in blocks:
        block_pos = i[0]
        if pos[0] > block_pos[0] and pos[0] < (block_pos[0] + block_size):
            if pos[1] > block_pos[1] and pos[1] < (block_pos[1] + block_size):
                active_color = i[1]


def fill_one_color(new_color, pos):
    for i in blocks:
        block_pos = i[0]
        if pos[0] > block_pos[0] and pos[0] < (block_pos[0] + block_size):
            if pos[1] > block_pos[1] and pos[1] < (block_pos[1] + block_size):
                color_to_change = i[1]
                for i in blocks:
                    if i[1] == color_to_change:
                        i[1] = new_color
                else:
                    fill_picture_button.active = False
                    break


def change_active_color(color):
    global active_color
    active_color_button.color = color
    active_color = color


def save():
    file = showFileNav()
    if len(file) == 0:
        return

    with open(file + ".txt", "w") as f:
        for i in blocks:
            f.write(str(i[1][0]) + " ")
            f.write(str(i[1][1]) + " ")
            f.write(str(i[1][2]) + "\n")


def load():
    file = showFileNav(True)
    if len(file) == 0:
        return

    with open(file, "r") as f:
        f = f.readlines()

    for index, i in enumerate(f):
        i = i.split(" ")
        blocks[index][1] = (int(i[0]), int(i[1]), int(i[2]))


def showFileNav(op=False):
    # Op is short form for open as open is a key word
    window = Tk()
    window.attributes("-topmost", True)
    window.withdraw()
    myFormats = [('Windows Text File', '*.txt')]
    if op:
        filename = askopenfilename(title="Open File", filetypes=myFormats)  # Ask the user which file they want to open
    else:
        filename = asksaveasfilename(title="Save File",
                                     filetypes=myFormats)  # Ask the user choose a path to save their file to
    return filename


def randomize_canvis():
    for i in blocks:
        i[1] = (randint(0,255), randint(0,255), randint(0,255))


def fill_canvis():
    for i in blocks:
        i[1] = (active_color)


def change_show_grid():
    global draw_grid_on_canvis

    if show_grid_button.active:
        show_grid_button.img = off_button_img
        draw_grid_on_canvis = False
    else:
        show_grid_button.img = on_button_img
        draw_grid_on_canvis = True


def settings():
    global run

    def redraw_setting_win():
        win.fill(WHITE)

        draw_text("Pixlar Art", middleX=True, size=60)
        draw_text("Show Grid", x=show_grid_button.x, y=show_grid_button.y - 20, size=25)
        settings_button.draw()
        show_grid_button.draw()

        pygame.display.update()

    while settings_button.active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                settings_button.active = False
        redraw_setting_win()


def custom_rgb_color():
    global run, active_color

    blue = 0
    color_window_X, color_window_Y = color_picker_button.x - 320, color_picker_button.y - 200

    while color_picker_button.active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                color_picker_button.active = False

        # x=[0], y=[1], width=[2], height=[3]
        slider = (color_window_X + 255, color_window_Y + blue, 45, 10)
        pygame.draw.rect(win, WHITE, (300, 0, 200, 45))

        draw_text("Pixlar Art", middleX=True, size=60)

        for color_button in all_color_buttons:
            color_button.draw()

        draw_text("Active Color", x=active_color_button.x - 30, y=active_color_button.y - 20, color=active_color)
        color_picker_button.draw()

        pygame.draw.rect(win, GRAY, (color_window_X, color_window_Y, 300, 255))
        pygame.draw.rect(win, (0, 0, 0), slider)

        for red in range(256):
            for green in range(256):
                pygame.draw.rect(win, (red, green, blue), (color_window_X + red, color_window_Y + green, 1, 1))

        pygame.draw.rect(win, BLACK, (color_window_X, color_window_Y, 300, 255), 2)

        if pygame.mouse.get_pressed()[0]:
            if pygame.mouse.get_pos()[0] > slider[0] and pygame.mouse.get_pos()[0] < (slider[0] + slider[2]):
                if pygame.mouse.get_pos()[1] > slider[1] and pygame.mouse.get_pos()[1] < (slider[1] + slider[3]):
                    blue = pygame.mouse.get_pos()[1] - color_window_Y - 5
                    if blue > 255 - slider[3]:
                        blue = 255 - slider[3]
                    elif blue < 0:
                        blue = 0

                elif pygame.mouse.get_pos()[1] > color_window_Y and pygame.mouse.get_pos()[1] < color_window_Y + 255:
                    blue = pygame.mouse.get_pos()[1] - color_window_Y - 5
                    if blue > 255 - slider[3]:
                        blue = 255 - slider[3]
                    elif blue < 0:
                        blue = 0

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if pos[0] > color_window_X and pos[0] < (color_window_X + 255):
                if pos[1] > color_window_Y and pos[1] < (color_window_Y + 255):
                    active_color = (pos[0] - color_window_X, pos[1] - color_window_Y, blue)
                    active_color_button.color = active_color
                    rainbow_color_button.active_color = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if (pos[0] < color_window_X) or (pos[0] > (color_window_X + 300)):
                color_picker_button.active = False
            if pos[1] < color_window_Y or pos[1] > (color_window_Y + 255):
                color_picker_button.active = False



        pygame.draw.rect(win, BLACK, (color_window_X + 255, color_window_Y, 45, 255), 2)
        pygame.display.update()


def redraw_win():
    win.fill(WHITE)
    draw_canvis()

    reset_button.draw()
    save_button.draw()
    load_button.draw()
    fill_button.draw()
    random_picture_button.draw()
    settings_button.draw()
    fill_picture_button.draw()
    color_picker_button.draw()

    draw_text("Pixlar Art", middleX=True, size=60)
    draw_text("Active Color", x=active_color_button.x - 30, y=active_color_button.y - 20, color=active_color)

    for color_button in all_color_buttons:
        color_button.draw()

    pygame.display.update()


reset_button = button("Clear", 30, HEIGHT- 100, 94, 34, 50, BLACK, clear_canvis)
save_button = button("Save", WIDTH/2 - 100, HEIGHT - 100, 85, 34, 50, BLACK, save)
load_button = button("Load", WIDTH/2, HEIGHT - 100, 85, 34, 50, BLACK, load)
fill_button = button("Fill", 30, HEIGHT - 50, 50, 34, 50, BLACK, fill_canvis)
random_picture_button = button("Ranom Picture", WIDTH/2 - 130, HEIGHT - 50, 248, 34, 50, BLACK, randomize_canvis)
fill_picture_button = button(img=pygame.transform.smoothscale(fill_img, (50, 50)), x=WIDTH - 200, y=HEIGHT- 100, width=50, height=50)

settings_button = button(img=pygame.transform.smoothscale(settings_img, (50, 50)), x=10, y=10, width=50, height=50, func=settings)
color_picker_button = button(img=pygame.transform.smoothscale(custom_color_picker_img, (50,50)), x=WIDTH-75, y=canvisY_start + 55 * 7, width=50, height=50, func=custom_rgb_color)


active_color_button = colors_button(active_color, WIDTH - 100, HEIGHT - 90, change_active_color)
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
gray_color_button = colors_button((100,100,100), random_color_button.x, blue_color_button.y + 55, change_active_color)
all_color_buttons.append(gray_color_button)
rainbow_color_button = colors_button(BLACK, random_color_button.x, gray_color_button.y + 55, change_active_color)
all_color_buttons.append(rainbow_color_button)

show_grid_button = button(img=on_button_img, x=200, y=100, width=80, height=50,func=change_show_grid)

get_block_pos()


def main():
    global run, timer, active_color, enter_settings

    while run:
        redraw_win()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if pygame.mouse.get_pressed()[0]:
            if not fill_picture_button.active:
                draw(pygame.mouse.get_pos(), active_color)
            else:
                fill_one_color(active_color, pygame.mouse.get_pos())

        elif pygame.mouse.get_pressed()[2]:
            draw(pygame.mouse.get_pos(), block_start_color)
        elif pygame.mouse.get_pressed()[1]:
            rainbow_color_button.active_color = False
            get_color_from_canvis(pygame.mouse.get_pos())
            active_color_button.color = active_color

        if timer <= 0:
            random_color_button.color = (randint(0,255), randint(0,255), randint(0,255))
            timer = 50
        elif timer % 5 == 0:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            rainbow_color_button.color = color
            if rainbow_color_button.active_color:
                active_color = color
                active_color_button.color = color
            timer -= 1
        else:
            timer -= 1

        if settings_button.active:
            settings()
            settings_button.active = False

main()
pygame.display.quit()
