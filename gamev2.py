import pygame
import sys
import pygame_gui

from pygame_gui.elements import UITextBox
from pygame_gui.core import ObjectID

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
manager = pygame_gui.UIManager((800, 600))
#Use this to display text
text_box = UITextBox('<font face=fira_code size=3 color=#FFFFFF>'
                     'This is a test for our user interface using pygame. It would allow us to display images,'
                     'show text, and buttons to allow users to choose what to say or do.'
                     '<br><br>'


                     '</font>',
                     pygame.Rect((10, 10), (780, 500)),
                     manager=manager,
                     object_id=ObjectID(class_id="@text_box", object_id="#text_box_1"))
text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR,
                                       params={'time_per_letter': 0.05,
                                               'time_per_letter_deviation': 0.02})
def showText(text):
    text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR,
                                       params={'time_per_letter': 0.05,
                                               'time_per_letter_deviation': 0.02})
    text_box.set_text(text)
def showTextButtons(text, x, y):
    surface = font.render(text, True, text_color)
    screen.blit(surface, (x, y))

#Use this to make a button
def choiceButton(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    showTextButtons(text, x + w/2 - len(text)*4, y + h/2 - 16)


def scene_one():
    screen.fill(background_color)
    showText("Hello, and welcome to Zombie Game! How many players are playing?")
    time_delta = clock.tick(60)/1000.0

    #manager.process_events(event)

    while True:
        time_delta = clock.tick(60)/1000.0
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
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(window_surface)
        choiceButton("Choice One s1", 50, 150, 700, 50, button_color)
        choiceButton("Choice Two s1", 50, 250, 700, 50, button_color)
        pygame.display.update()


def scene_two_1():
    screen.fill(background_color)
    showText("Scene 2 first choice Text")
    time_delta = clock.tick(60)/1000.0
    manager.update(time_delta)
    manager.draw_ui(window_surface)
    choiceButton("Choice 1 s2.1", 50, 150, 700, 50, button_color)
    choiceButton("Choice 2 s1.1", 50, 250, 700, 50, button_color)
    pygame.display.update()
    while True:
        time_delta = clock.tick(60)/1000.0
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
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(window_surface)
        choiceButton("go to scene_three_1", 50, 150, 700, 50, button_color)
        choiceButton("go to scene_three_2", 50, 250, 700, 50, button_color)
        pygame.display.update()


def scene_two_2():
    screen.fill(background_color)
    showText("Scene 2 second choice Text")
    time_delta = clock.tick(60)/1000.0
    manager.update(time_delta)
    manager.draw_ui(window_surface)
    choiceButton("choice 1 s2.2", 50, 150, 700, 50, button_color)
    choiceButton("choice 2 s2.2", 50, 250, 700, 50, button_color)
    pygame.display.update()
    while True:
        time_delta = clock.tick(60)/1000.0
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
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(window_surface)
        choiceButton("go to scene_four_1", 50, 150, 700, 50, button_color)
        choiceButton("go to scene_four_2", 50, 250, 700, 50, button_color)
        pygame.display.update()

clock = pygame.time.Clock()
while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        manager.process_events(event)

    window_surface.blit(background, (0, 0))

    pygame.display.update()
    time_delta = clock.tick(60)/1000.0

    manager.update(time_delta)

    manager.draw_ui(window_surface)

    scene_one()

