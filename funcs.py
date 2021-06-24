from classes import *
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename


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


def settings():
    global run

    while settings_button.active:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()

        win.fill(WHITE)

        draw_text("Pixlar Art", middleX=True, size=60)
        settings_button.draw()

        pygame.display.update()


reset_button = button("Clear", 30, HEIGHT- 100, 94, 34, 50, BLACK, clear_canvis)
save_button = button("Save", WIDTH/2 - 100, HEIGHT - 100, 85, 34, 50, BLACK, save)
load_button = button("Load", WIDTH/2, HEIGHT - 100, 85, 34, 50, BLACK, load)
fill_button = button("Fill", 30, HEIGHT - 50, 50, 34, 50, BLACK, fill_canvis)
random_picture_button = button("Ranom Picture", WIDTH/2 - 130, HEIGHT - 50, 248, 34, 50, BLACK, randomize_canvis)

settings_button = button(img=pygame.transform.smoothscale(pygame.image.load("settings.png"), (50, 50)), x=10, y=10, width=50, height=50, func=settings)

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
gray_color_button = colors_button(GRAY, random_color_button.x, blue_color_button.y + 55, change_active_color)
all_color_buttons.append(gray_color_button)
rainbow_color_button = colors_button(BLACK, random_color_button.x, gray_color_button.y + 55, change_active_color)
all_color_buttons.append(rainbow_color_button)


get_block_pos()

