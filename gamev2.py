import pygame
import sys
import pygame_gui
from pygame_gui.elements import UITextBox
from pygame_gui.core import ObjectID
from scene import Scene

pygame.init()
pygame.mixer.init()

# Load the music files
""" "Quinn's Song: A New Man" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/ """
startMusic = pygame.mixer.Sound("data/audio/Quinns Song-A New Man.mp3")
startMusic.set_volume(0.4)

""" "Metaphysik" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/ """
introMusic = pygame.mixer.Sound("data/audio/Metaphysik.mp3")
introMusic.set_volume(0.4)

""" "SCP-x3x (I am Not OK)" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/ """
scene17Music = pygame.mixer.Sound("data/audio/SCP-x3x.mp3")
scene17Music.set_volume(0.35)

""" "Unseen Horrors" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/ """
scene22Music = pygame.mixer.Sound("data/audio/Unseen Horrors.mp3")
scene22Music.set_volume(0.45)

""" "Awkward Meeting" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/ """
scene26Music = pygame.mixer.Sound("data/audio/Awkward Meeting.mp3")
scene26Music.set_volume(0.2)

# Play the first sound
startMusic.play()

# Set up screen and fonts
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game.py")
window_surface = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 28)

background_color = (0, 0, 0)
background = pygame.Surface((800, 600))
background.fill((6, 28, 31))
button_color = (8, 12, 9)
text_color = (107, 116, 118)
#hover_color = (52, 152, 219)

is_running = True

# Set up game variables
giveGun = False
shotgun = False
food = False
medicine = False
twoPlayer = False
destination = "gun store"
bitTwice = False
run = False
eatFood = False
useMedicine = False
keepGun = False
manager = pygame_gui.UIManager((800, 600))

# Use this to display text
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


scenes = [Scene("Hello, and welcome to Zombie Game! How many players are playing?",
                "1 Player", "2 Players", 1, 2, 2)]  # 0
scenes.append(
    Scene("This is an interactive story game that follows the journey of 2 characters. As the sole player, you will control both characters in different segments",
          "Continue",
          "Continue",
          3,
          3,
          1))  # 1
scenes.append(
    Scene("This is an interactive story game that follows the journey of 2 characters. Each player may choose which character they will play and control during their segments.",
          "Continue",
          "Continue",
          3,
          3,
          1))  # 2
scenes.append(
    Scene("Chapter 1: David",
          "Continue",
          "Continue",
          4,
          4,
          1,
          True,
          introMusic))  # 3
scenes.append(
    Scene("It has been months since the dead started to rise and the collapse of civilization. Millions have died in the chaos. Survivors cling to hope through reports of a safe haven being created by the government in Virginia.",
          "Continue",
          "Continue",
          5,
          5,
          1))  # 4
scenes.append(
    Scene("David and his young son Cole have remained hidden in their home, surviving on the food they managed to stock and the remains they could scavange from neighboring houses. But supplies are running short, and David decides to venture out and scavenge what he can from his deserted town.",
          "Continue",
          "Continue",
          6,
          6,
          1))  # 5
scenes.append(
    Scene("David: I'll be back soon Cole, I promise. Remember what we practiced, keep the noise down, lights off, and stay in the house.\nCole: But I should come with you, what if one of the monsters gets in here?",
          "Give Cole your pistol",
          "Tell him to hide",
          7,
          8,
          2))  # 6
scenes.append(
    Scene("David: Here, take this. Remember, it isn't a toy and should be your last resort. Remember what we practiced. I love you.",
          "Leave to search the town",
          "Leave to search the town",
          9,
          9,
          1))  # 7
scenes.append(
    Scene("David: Nothing is getting in here, we haven't seen them pass by in weeks and this place is boarded up tight. Everything will be fine, I promise.",
          "Leave to search the town",
          "Leave to search the town",
          9,
          9,
          1))  # 8
scenes.append(
    Scene("David leaves his home for the first time in months. He carefully makes his way from his neighborhood to the outskirts of the town, which appears deserted. He notices the gun store and grocery store both seem safe to check. Which should he search first?",
          "Gun Store",
          "Grocery Store",
          10,
          11,
          2))  # 9
scenes.append(
    Scene("Moving quietly, David makes his way into the gun store. It appears completely looted, but David remembers the owner of the store, an old drinking buddy, he always kept a sidearm hidden in case of a robbery. David inspects the cabinet under the front desk and finds a hidden sawed off shotgun with a few cases of ammo.",
          "Exit the Store",
          "Exit the Store",
          16,
          16,
          1))  # 10
scenes.append(
    Scene("Moving quietly, David enters the ransacked grocery store. After searching aisle after aisle, he finds a few cans of soup at the top of a shelf that must've been overlooked in the chaos.",
          "Continue Searching",
          "Exit the Store",
          12,
          16,
          2))  # 11
scenes.append(
    Scene("David continues to search, eventually ending up at the medicine section near the back of the store. To his surprise, he sees a bottle of antiobiotics for the taking. But it is blocked by a pile of zombie corpes. They look like they are dead for good, but you can never be too sure.",
          "Go for the medicine",
          "Exit the Store",
          13,
          16,
          2))  # 12
scenes.append(
    Scene("David slowly moves towards the medicine, doing his best to ignore the putrid smell and not disturb the dead. He opens up his backpack and reaches for the medicine when suddenly a zombie bursts out of the pile and lunges at him.",
          "Use gun to kill zombie",
          "Use knife to kill zombie",
          14,
          15,
          2,
          True,
          scene17Music))  # 13
scenes.append(
    Scene("David stumbles back and pulls out his gun. He takes a moment to line up his shot and pulls the trigger. The shot hits the zombie in the head, taking it down with little problem. David quickly grabs the medicine and heads for the exit, hoping the shot doesn't attract any more of them.",
          "Exit the store",
          "Exit the store",
          16,
          16,
          1))  # 14
scenes.append(
    Scene("David stumbles back and reaches for his knife. Before he can ready himself, the zombie grabs him and ferociously tries to bite at his neck. The contents of David's backpack fall to the floor in the struggle, and David narrowly manages to grab his knife and kill the zombie. He then takes the medicine, but the food he had gathered previously is ruined as the cans burst open and are spread into the filth along the floor.",
          "Exit the store",
          "Exit the store",
          16,
          16,
          1))  # 15
scenes.append(
    Scene("David approaches the exit.",
          "Continue",
          "Exit the store",
          17,
          17,
          1))  # 16
scenes.append(
    Scene("David approaches the exit and peaks his head out to survey the surrounding area. The street looks clear, and David heads outside towards the " + destination + ". Just as he nears his destination he turns a corner and is confronted by two zombies.",
          "Fight",
          "Run",
          18,
          19,
          2,
          True,
          scene17Music))  # 17
scenes.append(
    Scene("David reaches for his gun as the two zombies approach him. He manages to take one out before the other grabs ahold of him. It tackles him to the ground and tries to gnaw at his flesh. David tries to hold it back, but his energy is getting spent.",
          "Continue",
          "Continue",
          20,
          20,
          1))  # 18
scenes.append(
    Scene("David quickly turns around and sprints away as the fast moving zombies pursue him. If he can make it home, the defenses set up at the house should keep him safe",
          "Continue",
          "Continue",
          20,
          20,
          1))  # 19
scenes.append(
    Scene("Chapter 1: Cole",
          "Continue",
          "Continue",
          21,
          21,
          1,
          True,
          introMusic))  # 20
scenes.append(
    Scene("Cole anxiously awaits his fathers return and paces around the house. It is getting dark out, and Cole senses something must be wrong. Fearing for his father's safety, he decides to go looking for him.",
          "Continue",
          "Continue",
          22,
          22,
          1))  # 21
scenes.append(
    Scene("Cole follows his fathers path and heads towards the town. He eventually reaches the outskirts when he sees his father running towards him, pursued by two zombies.",
          "Continue",
          "Continue",
          23,
          23,
          1,
          True,
          scene22Music))  # 22
scenes.append(
    Scene("As David yells for Cole to run and get back to the house, the pair of zombies catch up to him and tackle him to the ground. Cole runs to help, but David shouts not to come any closer and stay safe.",
          "Try to help",
          "Stay back",
          24,
          25,
          2))  # 23
scenes.append(
    Scene("Cole pulls out the gun his father had trusted him with and takes aim. He fires multiple shots, but the zombies persist in their attack. With his last shot, he hits one of them directly in the head and kills it. David reaches for his knife, but this loosens his defense against the remaining zombie and it bites him on the arm. David screams in pain and use his free hand to stab the zombie and kill it for good.",
          "Continue",
          "Continue",
          26,
          26,
          1))  # 24
scenes.append(
    Scene("Afraid and unsure of what to do, Cole listens to his father and keeps his distance. With David's energy spent, David tries to reach for his knife as one zombie sinks its teeth into his leg and the other his arm. He screams in pain and in a burst of adrenaline, uses this moment to kill them for good.",
          "Continue",
          "Continue",
          26,
          26,
          1))  # 25
scenes.append(
    Scene("With the threat gone, Cole runs over to David and looks in shock at his wounds. They've heard over the radio that nobody has lasted more than a week after being bit.\nDavid: Listen, everything is going to be ok. I know things are scary right now but we need to get back to the house before its gets too dark.\nCole: Ok, let me help you.\nAs night falls, Cole and a weakened David make their way back home.",
          "Continue",
          "Continue",
          27,
          27,
          1,
          True,
          scene26Music))  # 26
scenes.append(
    Scene("They arrive home safely and sit down to talk.\nDavid: Cole, we don't know what is going to happen to me. I'm sorry you have to go through this. All that matters is that you are safe. I think it is best if we make our way to that refuge in Virginia. If we take the car we should make it within a few days.\nCole begins to feel a glimmer of hope.",
          "Ask if he could be cured",
          "Ask if it will be safe there",
          28,
          29,
          2))  # 27
scenes.append(
    Scene("Cole: It's been awhile, but I remember hearing them talk about treatments they were working on. We can get you help!\nDavid looks unsure\nDavid: I hope so, we'll see when we get there, but no matter what you will be safe.",
          "Continue",
          "Continue",
          30,
          30,
          1))  # 28
scenes.append(
    Scene("Cole: Do you really think we will be safe? The radio went silent awhile ago, we don't even know if that place is still around.\nDavid: We know the military had it running, they would defend it at all costs. I'm sure it will be ok.",
          "Continue",
          "Continue",
          30,
          30,
          1))  # 29
scenes.append(
    Scene("Cole looks at what David has brought back with him and notices he found another gun.",
          "Ask if you can keep a gun",
          "Let David keep the weapons",
          33,
          37,
          2))  # 30
scenes.append(
    Scene("David: Here, I know you're hungry, I was able to find some food.\nCole begins eating but notices his father isn't eating anything.\nCole: Why are you eating, aren't you hungry?\nDavid: I'm alright. I wasn't able to find much, you should keep your strength up.",
          "Share food with David",
          "Continue eating",
          34,
          37,
          2))  # 31
scenes.append(
    Scene("Cole looks at what David has brought back with him and notices he found some antibiotics.\nCole: You found medicine! This could help you, you need to take it.\nDavid: We aren't sure if that will do anything for me. That stuff is like gold these days, we should save it.",
          "Beg David to take it",
          "Agree to save it",
          35,
          36,
          2))  # 32
scenes.append(
    Scene("Cole: Now that we have a few guns, do you think I could keep one?\nDavid: You did good today, I wish you didn't have to but thanks for coming out to help me. We will need to keep practicing, but this belongs to you.\nDavid lets Cole keep a pistol.",
          "Continue",
          "Continue",
          37,
          37,
          1))  # 33
scenes.append(
    Scene("Cole: I'm not eating unless you do. You can't give up dad.\nCole passes David some food.\nDavid: Ok buddy, but if you are still hungry let me know.",
          "Continue",
          "Continue",
          37,
          37,
          1))  # 34
scenes.append(
    Scene("Cole: Please dad, this could really help you. If you can hang in there long enough we can get you help. Please take it.\nDavid: Ok bud, I'll take it.\nDavid takes the medicine.",
          "Continue",
          "Continue",
          37,
          37,
          1))  # 35
scenes.append(
    Scene("Cole: Fine, but if you get any worse you need to try and take this.\nCole puts away the medicine.",
          "Continue",
          "Continue",
          37,
          37,
          1))  # 36
scenes.append(
    Scene("After getting some sleep, David and Cole gather their supplies and pack them into their car. They don't have much fuel, but they should be able to get a good distance toward their destination. They say goodbye to their home and begin their journey.",
          "Continue",
          "Continue",
          38,
          38,
          1))  # 37
scenes.append(
    Scene("End of Chapter 1",
          "Continue",
          "Continue",
          39,
          39,
          1))  # 38


def showText(text):
    text_box.set_text(text)
    text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR,
                               params={'time_per_letter': 0.02,
                                       'time_per_letter_deviation': 0})


def showTextButtons(text, x, y):
    surface = font.render(text, True, text_color)
    screen.blit(surface, (x, y))

# Use this to make a button
def choiceButton(text, x, y, w, h, color):
    pygame.draw.rect(screen, text_color, (x - 0.1, y - 0.1, w + 2, h + 2))
    pygame.draw.rect(screen, color, (x, y, w, h))
    showTextButtons(text, x + w/2 - len(text)*5, y + h/2 - 10)

# Function used to update all variables related to decisions
def newChoice(sceneNum):
    global food, giveGun, shotgun, medicine, twoPlayer, destination, bitTwice, run, eatFood, useMedicine, keepGun
    # Chapter 1
    if (sceneNum == 2):
        twoPlayer = True
    if (sceneNum == 7):
        giveGun = True
    if (sceneNum == 10):
        shotgun = True
        destination = "grocery store"
    if (sceneNum == 11):
        food = True
    if (sceneNum == 14):
        medicine = True
    if (sceneNum == 15 or (sceneNum == 14 and giveGun == True)):
        food = False
        medicine = True
    if (sceneNum == 18 and (giveGun == True and shotgun == False)):
        bitTwice = True
    if (sceneNum == 19):
        run = True
    if (sceneNum == 19 and giveGun == False):
        bitTwice = True
    if (sceneNum == 33):
        keepGun = True
    if (sceneNum == 34):
        eatFood = True
    if (sceneNum == 35):
        useMedicine = True

# Checks if the text of the current scene should be updated based on previous decisions, 
# otherwise returns the scenes default text
def updateChoice(sceneNum):
    # Chapter 1
    if (sceneNum == 3 and twoPlayer == True):
        return "Chapter 1: David\nPlayer 1's turn!"
    if (sceneNum == 9 and giveGun == True):
        return "Now without his gun and armed with only a knife, David leaves his home for the first time in months. He carefully makes his way from his neighborhood to the outskirts of the town. He notices the gun store and grocery store both seem safe to check. Which should he search first?"
    if (sceneNum == 14 and giveGun == True):
        return "David stumbles back and instinctively reaches for his gun, but finds it missing and realizes he had given it to Cole. Before he can ready himself, the zombie grabs him and ferociously tries to bite at his neck. The contents of David's backpack fall to the floor in the struggle, and David narrowly manages to grab his knife and kill the zombie. He then takes the medicine, but the food he had gathered previously is ruined as the cans burst open and are spread into the filth along the floor."
    if (sceneNum == 16 and food == True and medicine == True):
        return "Having gathered food and medicine, David goes to exit the store."
    if (sceneNum == 16 and food == True and medicine == False):
        return "Having gathered some food, David goes to exit the store."
    if (sceneNum == 16 and food == False and medicine == True):
        return "Having gathered medicine, David goes to exit the store."
    if (sceneNum == 16 and shotgun == True):
        return "Having gathered a new gun and some ammo, David goes to exit the store."
    if (sceneNum == 17):
        return "David approaches the exit and peaks his head out to survey the surrounding area. The street looks clear, and David heads outside towards the " + destination + ". Just as he nears his destination he turns a corner and is confronted by two zombies."
    if (sceneNum == 18 and bitTwice == True):
        return "With no available gun, David pulls out his knife to defend himself. He tries to take out one of the zombies but the flesh hungry monsters manage to overpower him and tackle him to the ground. David uses all of his strength to hold them back, but things are looking grim."
    if (sceneNum == 22 and run == False and bitTwice == True):
        return "Cole follows his fathers path and heads towards the town. He reaches the outskirts when he hears yelling in the distance. He sprints into the town and sees his father struggling with two zombies."
    if (sceneNum == 22 and run == False and bitTwice == False):
        return "Cole follows his fathers path and heads towards the town. He reaches the outskirts when he hears yelling in the distance. He sprints into the town and sees his father struggling with a zombie."
    if (sceneNum == 23 and run == False and bitTwice == False):
        return "Cole continues to run towards his father to help but before he can get there the zombie sinks its teeth into his fathers arm. Cole screams in horror, and David yells for him to stay back."
    if (sceneNum == 23 and run == False and bitTwice == True):
        return "Cole continues to run towards his father to help but before he can get there one zombie sinks its teeth into his fathers arm and the other into his leg. Cole screams in horror, and David yells for him to stay back."
    if (sceneNum == 24 and giveGun == False and run == False):
        return "Unarmed and helpless, Cole quickly grabs an old wooden board on the street and runs to his father. He swings at the zombie with all his strength, but it is unaffected and remains focused on David. He finally unleashes a massave swing that stuns the zombie and gives David the chance to grab his knife and kill it for good."
    if (sceneNum == 24 and giveGun == True and run == False and bitTwice == False):
        return "Cole takes out the gun his father trusted him with and lines up his target. He fires multiple shots but the zombie is unafected. Down to his last shot, he fires into the Zombie's head and kills it for good."
    if (sceneNum == 24 and giveGun == True and run == False and bitTwice == True):
        return "Cole takes out the gun his father trusted him with and lines up his target. He fires multiple shots but the zombie is unafected. Down to his last shot, he fires into the Zombie's head and kills it for good. David uses this opportunity to grab his knife and kill the remaining zombie."
    if (sceneNum == 24 and run == True and giveGun == False):
        return "Unarmed and helpless, Cole quickly grabs an old wooden board on the street and runs to his father. He desperately tries to hit and distract the zombies but it is no use, as they remain fixated on David. With David's energy spent, David tries to reach for his knife as one zombie sinks its teeth into his leg and the other his arm. He screams in pain and in a burst of adrenaline, uses this momement to kill them as they bite into him."
    if (sceneNum == 25 and run == False and bitTwice == False):
        return "Afraid and unsure of what to do, Cole listens to his father and keeps his distance. David gains a burst of adrenaline and uses his free hand to finally grab his knife and kill the zombie for good."
    if (sceneNum == 25 and run == False and bitTwice == True):
        return "Afraid and unsure of what to do, Cole listens to his father and keeps his distance. With the zombies now distracted, David gains a burst of adrenaline and gets ahold of his knife and kill both zombies for good."
    if (sceneNum == 30 and medicine == True):
        runScene(32)
    if (sceneNum == 30 and medicine == False and food == True):
        runScene(31)
    return scenes[sceneNum].mainText

# main function that can be given a scene and will handle everything associated with displaying that scene
def runScene(sceneNum):
    if scenes[sceneNum].switchMusic:
        pygame.mixer.fadeout(3000)
        scenes[sceneNum].soundClip.play()

    screen.fill(background_color)
    showText(updateChoice(sceneNum))
    time_delta = clock.tick(60)/1000.0

    button1X = 50
    button1Y = 450
    if (scenes[sceneNum].numButtons == 1):
        button1X = 80 + 150
        button1Y = 450

    # manager.process_events(event)
    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if x > button1X and x < (button1X + 350) and y > button1Y and y < (button1Y + 40):
                        newChoice(scenes[sceneNum].sceneOption1Index)
                        runScene(scenes[sceneNum].sceneOption1Index)
                    elif x > 420 and x < 770 and y > 450 and y < 490 and scenes[sceneNum].numButtons == 2:
                        newChoice(scenes[sceneNum].sceneOption2Index)
                        runScene(scenes[sceneNum].sceneOption2Index)
            manager.process_events(event)
        
        manager.update(time_delta)
        manager.draw_ui(window_surface)
        choiceButton(scenes[sceneNum].button1Text,
                    button1X, button1Y, 325, 40, button_color)
        if scenes[sceneNum].numButtons == 2:
            choiceButton(scenes[sceneNum].button2Text,
                        425, 450, 325, 40, button_color)
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
