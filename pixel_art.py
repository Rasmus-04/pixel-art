from funcs import *


def redraw_win():
    win.fill(WHITE)
    draw_canvis()

    reset_button.draw()
    save_button.draw()
    load_button.draw()
    fill_button.draw()
    random_picture_button.draw()
    settings_button.draw()

    draw_text("Pixlar Art", middleX=True, size=60)

    draw_text("Active Color", x=active_color_button.x - 30, y=active_color_button.y - 20, color=active_color)

    for color_button in all_color_buttons:
        color_button.draw()

    pygame.display.update()



def main():
    global run, timer, active_color, enter_settings

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