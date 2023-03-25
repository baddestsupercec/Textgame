import pygame
import sys

pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game.py")
window_surface = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 32)
text_color = (255, 255, 255)
background_color = (0, 0, 0)
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))
button_color = (41, 128, 185)
hover_color = (52, 152, 219)

is_running = True

#Use this to display text
def showText(text, x, y):
    surface = font.render(text, True, text_color)
    screen.blit(surface, (x, y))

#Use this to make a button
def choiceButton(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    showText(text, x + w/2 - len(text)*4, y + h/2 - 16)


def scene_one():
    screen.fill(background_color)
    showText("Scene One Text", 50, 50)
    choiceButton("Choice One s1", 50, 150, 700, 50, button_color)
    choiceButton("Choice Two s1", 50, 250, 700, 50, button_color)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if x > 50 and x < 750 and y > 150 and y < 200:
                        scene_two_1()
                    elif x > 50 and x < 750 and y > 250 and y < 300:
                        scene_two_2()
        pygame.display.update()


def scene_two_1():
    screen.fill(background_color)
    showText("Scene 2 first choice Text", 50, 50)
    choiceButton("Choice 1 s2.1", 50, 150, 700, 50, button_color)
    choiceButton("Choice 2 s1.1", 50, 250, 700, 50, button_color)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if x > 50 and x < 750 and y > 150 and y < 200:
                        #go to scene_three_1
                        showText("go to scene_three_1", 50, 50)
                    elif x > 50 and x < 750 and y > 250 and y < 300:
                        #go to scene_three_2
                        showText("go to scene_three_2", 50, 50)

        pygame.display.update()


def scene_two_2():
    screen.fill(background_color)
    showText("Scene 2 second choice Text", 50, 50)
    choiceButton("choice 1 s2.2", 50, 150, 700, 50, button_color)
    choiceButton("choice 2 s2.2", 50, 250, 700, 50, button_color)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if x > 50 and x < 750 and y > 150 and y < 200:
                        # go to scene_three_1
                        showText("go to scene_four_1", 50, 50)
                    elif x > 50 and x < 750 and y > 250 and y < 300:
                        # go to scene_three_2
                        showText("go to scene_four_2", 50, 50)

        pygame.display.update()


while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window_surface.blit(background, (0, 0))

    pygame.display.update()
    scene_one()

