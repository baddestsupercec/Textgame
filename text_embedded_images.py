import pygame
import pygame_gui

from pygame_gui.elements import UITextBox
from pygame_gui.core import ObjectID

pygame.init()


pygame.display.set_caption('Embedding images in Text Boxes')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/embedded_images_theme.json')

background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour('dark_bg'))


text_box = UITextBox('<font face=fira_code size=3 color=#FFFFFF>'
                     ''
                     '<img src="data/images/test_images/zombie.jpg" '
                     'float=left '
                     'padding="5px 10px 5px 5px">'
                     'This is a test for our user interface using pygame. It would allow us to display images,'
                     'show text, and buttons to allow users to choose what to say or do.'
                     '<br><br>'


                     '</font>',
                     pygame.Rect((10, 10), (780, 300)),
                     manager=manager,
                     object_id=ObjectID(class_id="@text_box", object_id="#text_box_1"))

position = ((20),(310))
pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position,(200,150)),text='Option 1', manager=manager, object_id='test')
position = ((300),(310))
pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position,(200,150)),text='Option 2', manager=manager, object_id='test')
position = ((600),(310))
pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position,(200,150)),text='Option 3', manager=manager, object_id='test')

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
