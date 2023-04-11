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

giveGun = False
shotgun = False
food = False
medicine = False

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
                                       params={'time_per_letter': 0.03,
                                               'time_per_letter_deviation': 0.02})


#Scenes list holds all scenes in the game. Each entry is a tuple with the main text, button 1 text, button 2 text, and
#the indices of the scenes in the list each button should link to when pressed.
#Last number in tuple is 1 or 2 depending on if that scene should use 1 button or 2 buttons
scenes = [("Hello, and welcome to Zombie Game! How many players are playing?","1 Player","2 Players",1,2,2)] #0
scenes.append(("This is an interactive story game that follows the journey of 2 characters. As the sole player, you will control both characters in different segments","Continue","Continue",3,3,1)) #1
scenes.append(("This is an interactive story game that follows the journey of 2 characters. Each player may choose which character they will play and control during their segments.","Continue","Continue",3,3,1)) #2
scenes.append(("Chapter 1: David","Continue","Continue",4,4,1)) #3
scenes.append(("It has been months since the dead started to rise and the collapse of civilization. Millions have died in the chaos. Survivors cling to hope through reports of a safe haven being created by the government in Virginia.",
    "Continue",
    "Continue",
    5,
    5,
    1)) #4
scenes.append(("David and his young son Cole have remained hidden in their home, surviving on the food they managed to stock and the remains they could scavange from neighboring houses. But supplies are running short, and David decides to venture out and scavenge what he can from his deserted town.",
    "Continue",
    "Continue",
    6,
    6,
    1)) #5
scenes.append(("David: I'll be back soon Cole, I promise. Remember what we practiced, keep the noise down, lights off, and stay in the house.\nCole: But I should come with you, what if one of the monsters gets in here?",
    "Give Cole your pistol",
    "Tell him to hide",
    7,
    8,
    2)) #6
scenes.append(("David: Here, take this. Remember, it isn't a toy and should be your last resort. Remember what we practiced. I love you.",
    "Leave to search the town",
    "Leave to search the town",
    9,
    9,
    1)) #7
scenes.append(("David: Nothing is getting in here, we haven't seen them pass by in weeks and this place is boarded up tight. Everything will be fine, I promise.",
    "Leave to search the town",
    "Leave to search the town",
    9,
    9,
    1)) #8
scenes.append(("David leaves his home for the first time in months. He carefully makes his way from his neighborhood to the outskirts of the town, which appears deserted. He notices the gun store and grocery store both seem safe to check. Which should he search first?",
    "Gun Store",
    "Grocery Store",
    10,
    11,
    2)) #9
scenes.append(("Moving quietly, David makes his way into the gun store. It appears completely looted, but David remembers the owner of the store, an old drinking buddy, he always kept a sidearm hidden in case of a robbery. David inspects the cabinet under the front desk and finds a hidden sawed off shotgun with a few cases of ammo.",
    "Exit the Store",
    "Exit the Store",
    16,
    16,
    1)) #10
scenes.append(("Moving quietly, David enters the ransacked grocery store. After searching aisle after aisle, he finds a few cans of soup at the top of a shelf that must've been overlooked in the chaos.",
    "Continue Searching",
    "Exit the Store",
    12,
    16,
    2)) #11
scenes.append(("David continues to search, eventually ending up at the medicine section near the back of the store. To his surprise, he sees a bottle of antiobiotics for the taking. But it is blocked by a pile of zombie corpes. They look like they are dead for good, but you can never be too sure.",
    "Go for the medicine",
    "Exit the Store",
    13,
    16,
    2)) #12
scenes.append(("David slowly moves towards the medicine, doing his best to ignore the putrid smell and not disturb the dead. He opens up his backpack and reaches for the medicine when suddenly a zombie bursts out of the pile and lunges at him.",
    "Use gun to kill zombie",
    "Use knife to kill zombie",
    14,
    15,
    2)) #13
scenes.append(("David stumbles back and pulls out his gun. He takes a moment to line up his shot and pulls the trigger. The shot hits the zombie in the head, taking it down with little problem. David quickly grabs the medicine and heads for the exit, hoping the shot doesn't attract any more of them.",
    "Exit the store",
    "Exit the store",
    16,
    16,
    1)) #14
scenes.append(("David stumbles back and reaches for his knife. Before he can ready himself, the zombie grabs him and ferociously tries to bite at his neck. The contents of David's backpack fall to the floor in the struggle, and David narrowly manages to grab his knife and kill the zombie. He then takes the medicine, but the food he had gathered previously is ruined as the cans burst open and are spread into the filth along the floor.",
    "Exit the store",
    "Exit the store",
    16,
    16,
    1)) #15
scenes.append(("Leave Store.",
    "Exit the store",
    "Exit the store",
    17,
    17,
    1)) #16
    

def showText(text):
    text_box.set_text(text)
    text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR,
                                       params={'time_per_letter': 0.03,
                                               'time_per_letter_deviation': 0.02})
def showTextButtons(text, x, y):
    surface = font.render(text, True, text_color)
    screen.blit(surface, (x, y))

#Use this to make a button
def choiceButton(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    showTextButtons(text, x + w/2 - len(text)*4, y + h/2 - 16)

#Function used to update all variables related to decisions
def newChoice(sceneNum):
    global food
    global giveGun
    global shotgun
    global medicine
    if(sceneNum==7):
        giveGun = True
    if(sceneNum==10):
        shotgun = True
    if(sceneNum==11):
        food = True
    if(sceneNum==14):
        medicine = True
    if(sceneNum==15 or (sceneNum==14 and giveGun == True)):
        food = False
        medicine = True

#Checks if the text of the current scene should be updated based on previous decisions, otherwise returns the scenes default text
def updateChoice(sceneNum):
    if(sceneNum == 9 and giveGun == True):
        return "Now without his gun and armed with only a knife, David leaves his home for the first time in months. He carefully makes his way from his neighborhood to the outskirts of the town. He notices the gun store and grocery store both seem safe to check. Which should he search first?"
    if(sceneNum == 14 and giveGun == True):
        return "David stumbles back and instinctively reaches for his gun, but finds it missing and realizes he had given it to Cole. Before he can ready himself, the zombie grabs him and ferociously tries to bite at his neck. The contents of David's backpack fall to the floor in the struggle, and David narrowly manages to grab his knife and kill the zombie. He then takes the medicine, but the food he had gathered previously is ruined as the cans burst open and are spread into the filth along the floor."
    if(sceneNum == 16 and food == True and medicine == True):
        return "Having gathered food and medicine, David goes to exit the store."
    if(sceneNum == 16 and food == True and medicine == False):
        return "Having gathered some food , David goes to exit the store."
    if(sceneNum == 16 and food == False and medicine == True):
        return "Having gathered medicine, David goes to exit the store."
    if(sceneNum == 16 and shotgun == True):
        return "Having gathered a new gun and some ammo, David goes to exit the store."
    return scenes[sceneNum][0]

#main function that can be given a scene and will handle everything associated with displaying that scene
def runScene(sceneNum):
    screen.fill(background_color)
    showText(updateChoice(sceneNum))
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
                    if x > 50 and x < 750 and y > 200 and y < 250:
                        newChoice(scenes[sceneNum][3])
                        runScene(scenes[sceneNum][3])
                    elif x > 50 and x < 750 and y > 300 and y < 350 and scenes[sceneNum][5]==2:
                        newChoice(scenes[sceneNum][4])
                        runScene(scenes[sceneNum][4])
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(window_surface)
        choiceButton(scenes[sceneNum][1], 50, 200, 700, 50, button_color)
        if scenes[sceneNum][5]==2:
            choiceButton(scenes[sceneNum][2], 50, 300, 700, 50, button_color)
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

    runScene(0)

