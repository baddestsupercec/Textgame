import argparse
import pygame
import sys
import pygame_gui
import os
import shutil
from PIL import Image
from pygame_gui.elements import UITextBox
from pygame_gui.core import ObjectID
from scene import Scene
from image_generator_free import image_generator


parser = argparse.ArgumentParser()

parser.add_argument(
    "--api-url",
    type=str,
    help="URL of API",
    default="http://127.0.0.1:7861",
)
args = parser.parse_args()

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
# background.fill((6, 28, 31))
button_color = (17, 21, 24)
button_hover_color = (168, 172, 172)
text_color = (87, 95, 96)

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
day = False
manager = pygame_gui.UIManager((800, 600))
images_dir = "data/images/tmp/"
if not os.path.isdir(images_dir):
    os.mkdir(images_dir)
ig = image_generator.image_generator(
    img_write_dir=images_dir, api_url=f"{args.api_url}/sdapi/v1/txt2img"
)

# Use this to display text
text_box = UITextBox(
    "<font face=fira_code size=3 color=#FFFFFF>"
    "This is a test for our user interface using pygame. It would allow us to display images,"
    "show text, and buttons to allow users to choose what to say or do."
    "<br><br>"
    "</font>",
    pygame.Rect((10, 10), (780, 200)),
    manager=manager,
    object_id=ObjectID(class_id="@text_box", object_id="#text_box_1"),
)


scenes = [
    Scene(
        "Hello, and welcome to Zombie Game! How many players are playing?",
        "1 Player",
        "2 Players",
        1,
        2,
        2,
    )
]  # 0
scenes.append(
    Scene(
        "This is an interactive story game that follows the journey of 2 characters. As the sole player, you will control both characters in different segments",
        "Continue",
        "Continue",
        3,
        3,
        1,
    )
)  # 1
scenes.append(
    Scene(
        "This is an interactive story game that follows the journey of 2 characters. Each player may choose which character they will play and control during their segments.",
        "Continue",
        "Continue",
        3,
        3,
        1,
    )
)  # 2
scenes.append(
    Scene("Chapter 1: David", "Continue", "Continue", 4, 4, 1, True, introMusic)
)  # 3
scenes.append(
    Scene(
        "It has been months since the dead started to rise and the collapse of civilization. Millions have died in the chaos. Survivors cling to hope through reports of a safe haven being created by the government in Virginia.",
        "Continue",
        "Continue",
        5,
        5,
        1,
    )
)  # 4
scenes.append(
    Scene(
        "David and his young son Cole have remained hidden in their home, surviving on the food they managed to stock and the remains they could scavange from neighboring houses. But supplies are running short, and David decides to venture out and scavenge what he can from his deserted town.",
        "Continue",
        "Continue",
        6,
        6,
        1,
    )
)  # 5
scenes.append(
    Scene(
        "David: I'll be back soon Cole, I promise. Remember what we practiced, keep the noise down, lights off, and stay in the house.\nCole: But I should come with you, what if one of the monsters gets in here?",
        "Give Cole your pistol",
        "Tell him to hide",
        7,
        8,
        2,
    )
)  # 6
scenes.append(
    Scene(
        "David: Here, take this. Remember, it isn't a toy and should be your last resort. Remember what we practiced. I love you.",
        "Leave to search the town",
        "Leave to search the town",
        9,
        9,
        1,
    )
)  # 7
scenes.append(
    Scene(
        "David: Nothing is getting in here, we haven't seen them pass by in weeks and this place is boarded up tight. Everything will be fine, I promise.",
        "Leave to search the town",
        "Leave to search the town",
        9,
        9,
        1,
    )
)  # 8
scenes.append(
    Scene(
        "David leaves his home for the first time in months. He carefully makes his way from his neighborhood to the outskirts of the town, which appears deserted. He notices the gun store and grocery store both seem safe to check. Which should he search first?",
        "Gun Store",
        "Grocery Store",
        10,
        11,
        2,
    )
)  # 9
scenes.append(
    Scene(
        "Moving quietly, David makes his way into the gun store. It appears completely looted, but David remembers the owner of the store, an old drinking buddy, he always kept a sidearm hidden in case of a robbery. David inspects the cabinet under the front desk and finds a hidden sawed off shotgun with a few cases of ammo.",
        "Exit the Store",
        "Exit the Store",
        16,
        16,
        1,
    )
)  # 10
scenes.append(
    Scene(
        "Moving quietly, David enters the ransacked grocery store. After searching aisle after aisle, he finds a few cans of soup at the top of a shelf that must've been overlooked in the chaos.",
        "Continue Searching",
        "Exit the Store",
        12,
        16,
        2,
    )
)  # 11
scenes.append(
    Scene(
        "David continues to search, eventually ending up at the medicine section near the back of the store. To his surprise, he sees a bottle of antiobiotics for the taking. But it is blocked by a pile of zombie corpes. They look like they are dead for good, but you can never be too sure.",
        "Go for the medicine",
        "Exit the Store",
        13,
        16,
        2,
    )
)  # 12
scenes.append(
    Scene(
        "David slowly moves towards the medicine, doing his best to ignore the putrid smell and not disturb the dead. He opens up his backpack and reaches for the medicine when suddenly a zombie bursts out of the pile and lunges at him.",
        "Use gun to kill zombie",
        "Use knife to kill zombie",
        14,
        15,
        2,
        True,
        scene17Music,
    )
)  # 13
scenes.append(
    Scene(
        "David stumbles back and pulls out his gun. He takes a moment to line up his shot and pulls the trigger. The shot hits the zombie in the head, taking it down with little problem. David quickly grabs the medicine and heads for the exit, hoping the shot doesn't attract any more of them.",
        "Exit the store",
        "Exit the store",
        16,
        16,
        1,
    )
)  # 14
scenes.append(
    Scene(
        "David stumbles back and reaches for his knife. Before he can ready himself, the zombie grabs him and ferociously tries to bite at his neck. The contents of David's backpack fall to the floor in the struggle, and David narrowly manages to grab his knife and kill the zombie. He then takes the medicine, but the food he had gathered previously is ruined as the cans burst open and are spread into the filth along the floor.",
        "Exit the store",
        "Exit the store",
        16,
        16,
        1,
    )
)  # 15
scenes.append(
    Scene("David approaches the exit.", "Continue", "Exit the store", 17, 17, 1)
)  # 16
scenes.append(
    Scene(
        "David approaches the exit and peaks his head out to survey the surrounding area. The street looks clear, and David heads outside towards the "
        + destination
        + ". Just as he nears his destination he turns a corner and is confronted by two zombies.",
        "Fight",
        "Run",
        18,
        19,
        2,
        True,
        scene17Music,
    )
)  # 17
scenes.append(
    Scene(
        "David reaches for his gun as the two zombies approach him. He manages to take one out before the other grabs ahold of him. It tackles him to the ground and tries to gnaw at his flesh. David tries to hold it back, but his energy is getting spent.",
        "Continue",
        "Continue",
        20,
        20,
        1,
    )
)  # 18
scenes.append(
    Scene(
        "David quickly turns around and sprints away as the fast moving zombies pursue him. If he can make it home, the defenses set up at the house should keep him safe",
        "Continue",
        "Continue",
        20,
        20,
        1,
    )
)  # 19
scenes.append(
    Scene("Chapter 1: Cole", "Continue", "Continue", 21, 21, 1, True, introMusic)
)  # 20
scenes.append(
    Scene(
        "Cole anxiously awaits his fathers return and paces around the house. It is getting dark out, and Cole senses something must be wrong. Fearing for his father's safety, he decides to go looking for him.",
        "Continue",
        "Continue",
        22,
        22,
        1,
    )
)  # 21
scenes.append(
    Scene(
        "Cole follows his fathers path and heads towards the town. He eventually reaches the outskirts when he sees his father running towards him, pursued by two zombies.",
        "Continue",
        "Continue",
        23,
        23,
        1,
        True,
        scene22Music,
    )
)  # 22
scenes.append(
    Scene(
        "As David yells for Cole to run and get back to the house, the pair of zombies catch up to him and tackle him to the ground. Cole runs to help, but David shouts not to come any closer and stay safe.",
        "Try to help",
        "Stay back",
        24,
        25,
        2,
    )
)  # 23
scenes.append(
    Scene(
        "Cole pulls out the gun his father had trusted him with and takes aim. He fires multiple shots, but the zombies persist in their attack. With his last shot, he hits one of them directly in the head and kills it. David reaches for his knife, but this loosens his defense against the remaining zombie and it bites him on the arm. David screams in pain and use his free hand to stab the zombie and kill it for good.",
        "Continue",
        "Continue",
        26,
        26,
        1,
    )
)  # 24
scenes.append(
    Scene(
        "Afraid and unsure of what to do, Cole listens to his father and keeps his distance. With David's energy spent, David tries to reach for his knife as one zombie sinks its teeth into his leg and the other his arm. He screams in pain and in a burst of adrenaline, uses this moment to kill them for good.",
        "Continue",
        "Continue",
        26,
        26,
        1,
    )
)  # 25
scenes.append(
    Scene(
        "With the threat gone, Cole runs over to David and looks in shock at his wounds. They've heard over the radio that nobody has lasted more than a week after being bit.\nDavid: Listen, everything is going to be ok. I know things are scary right now but we need to get back to the house before its gets too dark.\nCole: Ok, let me help you.\nAs night falls, Cole and a weakened David make their way back home.",
        "Continue",
        "Continue",
        27,
        27,
        1,
        True,
        scene26Music,
    )
)  # 26
scenes.append(
    Scene(
        "They arrive home safely and sit down to talk.\nDavid: Cole, we don't know what is going to happen to me. I'm sorry you have to go through this. All that matters is that you are safe. I think it is best if we make our way to that refuge in Virginia. If we take the car we should make it within a few days.\nCole begins to feel a glimmer of hope.",
        "Ask if he could be cured",
        "Ask if it will be safe there",
        28,
        29,
        2,
    )
)  # 27
scenes.append(
    Scene(
        "Cole: It's been awhile, but I remember hearing them talk about treatments they were working on. We can get you help!\nDavid looks unsure\nDavid: I hope so, we'll see when we get there, but no matter what you will be safe.",
        "Continue",
        "Continue",
        30,
        30,
        1,
    )
)  # 28
scenes.append(
    Scene(
        "Cole: Do you really think we will be safe? The radio went silent awhile ago, we don't even know if that place is still around.\nDavid: We know the military had it running, they would defend it at all costs. I'm sure it will be ok.",
        "Continue",
        "Continue",
        30,
        30,
        1,
    )
)  # 29
scenes.append(
    Scene(
        "Cole looks at what David has brought back with him and notices he found another gun.",
        "Ask if you can keep a gun",
        "Let David keep the weapons",
        33,
        37,
        2,
    )
)  # 30
scenes.append(
    Scene(
        "David: Here, I know you're hungry, I was able to find some food.\nCole begins eating but notices his father isn't eating anything.\nCole: Why aren't you eating, aren't you hungry?\nDavid: I'm alright. I wasn't able to find much, you should keep your strength up.",
        "Share food with David",
        "Continue eating",
        34,
        37,
        2,
    )
)  # 31
scenes.append(
    Scene(
        "Cole looks at what David has brought back with him and notices he found some antibiotics.\nCole: You found medicine! This could help you, you need to take it.\nDavid: We aren't sure if that will do anything for me. That stuff is like gold these days, we should save it.",
        "Beg David to take it",
        "Agree to save it",
        35,
        36,
        2,
    )
)  # 32
scenes.append(
    Scene(
        "Cole: Now that we have a few guns, do you think I could keep one?\nDavid: You did good today, I wish you didn't have to but thanks for coming out to help me. We will need to keep practicing, but this belongs to you.\nDavid lets Cole keep a pistol.",
        "Continue",
        "Continue",
        37,
        37,
        1,
    )
)  # 33
scenes.append(
    Scene(
        "Cole: I'm not eating unless you do. You can't give up dad.\nCole passes David some food.\nDavid: Ok buddy, but if you are still hungry let me know.",
        "Continue",
        "Continue",
        37,
        37,
        1,
    )
)  # 34
scenes.append(
    Scene(
        "Cole: Please dad, this could really help you. If you can hang in there long enough we can get you help. Please take it.\nDavid: Ok bud, I'll take it.\nDavid takes the medicine.",
        "Continue",
        "Continue",
        37,
        37,
        1,
    )
)  # 35
scenes.append(
    Scene(
        "Cole: Fine, but if you get any worse you need to try and take this.\nCole puts away the medicine.",
        "Continue",
        "Continue",
        37,
        37,
        1,
    )
)  # 36
scenes.append(
    Scene(
        "After getting some sleep, David and Cole gather their supplies and pack them into their car. They don't have much fuel, but they should be able to get a good distance toward their destination. They say goodbye to their home and begin their journey.",
        "Continue",
        "Continue",
        38,
        38,
        1,
    )
)  # 37
scenes.append(Scene("End of Chapter 1", "Continue", "Continue", 39, 39, 1))  # 38

# -----------------------------------------------------------Chapter 2-------------------------------------------
scenes.append(
    Scene("Chapter 2: David",
          "Continue",
          "Continue",
          40,
          40,
          1))  # 39
scenes.append(
    Scene("Virginia isn't far, but with limited food, water, and fuel, the trip was risky. \nThe empty roads only made the situation more sinister.",
          "Continue",
          "Continue",
          41,
          41,
          1))  # 40
scenes.append(
    Scene("David and Cole reach a small, abandoned town.\nDavid: We should start looking for fuel. We can't afford to run out before reaching Virginia."
          "\nUp ahead there is a gasoline station cluttered with abandoned cars.",
          "Try to siphon fuel from the cars",
          "Try to use the fuel pump",
          42,
          43,
          2))  # 41

scenes.append(
    Scene("David: You stay here Cole, and look out for any zombies. I'm going to try to get some fuel from those cars over there. "
          "\nCole: I know you've already been bit, but be careful. If you get bit again, it will only make your condition worse."
          "\nThe streets look calm, but there is an eerie feeling in the air",
          "Continue",
          "Continue",
          44,
          44,
          1))  # 42
scenes.append(
    Scene("David: You stay here Cole, and look out for any zombies. I'm going to try to get some fuel from the fuel pump."
          "\nCole: I know you've already been bit, but be careful. If you get bit again, it will only make your condition worse."
          "\nThe streets look calm, but there is an eerie feeling in the air",
          "Continue",
          "Continue",
          45,
          45,
          1))  # 43

scenes.append(
    Scene("David takes a deep breath before getting out of the car. It hasn't been long, but it's like he can already feel the virus running in his veins."
          "\nDavid works quickly to siphon fuel from the abandoned cars, but there isn't much left. Still, he'll take what he can get.",
          "Continue",
          "Continue",
          46,
          46,
          1))  # 44
scenes.append(
    Scene("David takes a deep breath before getting out of the car. It hasn't been long, but it's like he can already feel the virus running in his veins."
          "\nDavid attempts to recover some gasoline form the fuel pump, but quickly realizes there is none left. David needs to act quickly or risk getting attacked by a zombie again.",
          "Try to siphon fuel from the cars",
          "Try to siphon fuel from the cars",
          46,
          46,
          1))  # 45
scenes.append(
    Scene("As David is still attempting to fuel their car, there is a sudden noise from behind an abandoned car."
          "\nCole: Dad! There's a zombie coming!"
          "\nSure enough, a zombie approaches David although the zombie is slow and appears to be injured."
          "\nDavid immediately reaches for his weapon.",
          "Continue",
          "Continue",
          47,
          47,
          1))  # 46
scenes.append(
    Scene("It shouldn't take much to defeat this zombie, but David can not afford to take any chances."
          "\nWith little hesitation, David launches at the zombie with his knife",
          "Aim for the torso",
          "Aim for the neck",
          48,
          49,
          2))  # 47
scenes.append(
    Scene("David stabs the zombie right in the chest. Immediately, the zombie leans forward and opens its mouth to bite David on the shoulder."
          "\nCole: Dad, watch out!",
          "Use the gun",
          "Run away",
          50,
          51,
          2))  # 48
scenes.append(
    Scene("David stabs the zombie right in the neck. Immediately, the already-injured zombie stumbles back and falls. "
          "\nToo weak to move, the zombie is no longer a threat. David finishes up fueling the car, and their trip to Virginia continues.",
          "Continue",
          "Continue",
          52,
          52,
          1))  # 49
scenes.append(
    Scene("This zombie is proving to be more of a threat that anticipated. David pulls out his gun and fires a single shot to the head. The zombie stumbles back and lies still."
          "\nDavid finishes up fueling the car, and their trip to Virginia continues.",
          "Continue",
          "Continue",
          52,
          52,
          1))  # 50
scenes.append(
    Scene("With no chance to finish fueling the car, David runs back into the car and shuts the door. He can not risk getting bit again if he wants to get his son to Virginia."
          "\nDavid checks the fuel gauge, at least he was able to fill it up half way. David and Cole's trip to Virginia continues.",
          "Continue",
          "Continue",
          52,
          52,
          1))  # 51

scenes.append(Scene("End of Chapter 2", "Continue", "Continue", 53, 53, 1))  # 52

#-----------------------------------------------Chapter 3-----------------------------------------------
scenes.append(
    Scene("Chapter 3: David",
          "Continue",
          "Continue",
          54,
          54,
          1))  # 53
scenes.append(
    Scene("As David continues the drive to Virginia, he notices his hands shaking and his vision turning yellow. He tries to shake it off to hopefully "
          "reach their destination, for both of their sakes.",
          "Continue",
          "Continue",
          55,
          55,
          1))  # 54
scenes.append(
    Scene("David continues to struggle driving the car. The road has been relatively free of crashed cars and zombies thus far, but David"
          " continues to swerve and narrowly miss obstacles. ",
          "Ask Cole take over driving the car",
          "Ignore your condition",
          56,
          57,
          2))  # 55
scenes.append(
    Scene("David is relieved that Cole has taken over driving. His mind fades into happy thoughts of teaching Cole the fundamentals of driving."
          " Never did he think that Cole would need to use his skills for a time like this. ",
          "Continue",
          "Continue",
          59,
          59,
          1))  # 56
scenes.append(
    Scene("David continues to get drowsier. His head starts to spin and his vision goes green. Suddenly, he wakes to his son shouting.",
          "Continue",
          "Continue",
          58,
          58,
          1))  # 57
scenes.append(
    Scene("David looks up in horror with renewed clarity to see his car heading directly into a tree. As the car slams into the tree, David can"
          " only think of the previous decisions he has made. The tree begins to fall, but with nobody alive around, one can only wonder if it made"
          " any sound at all",
          "Exit Game",
          "Exit Game",
          75, #FIXME
          75, #FIXME
          1))  # 58
scenes.append(
    Scene("David wakes up to Cole vigorously shaking him. He notices a considerable amount of time has passed, as the sky is almost dark. "
          "A quick survey of the dash board shows the car has run out of gas. With no other cars in sight, it is obvious to both that they"
          " must continue on foot.",
          "Ask Cole to take you with him",
          "Ask Cole to leave you behind",
          60,
          60,
          2))  # 59
scenes.append(
    Scene("Cole has no intentions of leaving his father behind. David watches his son scurry about, collecting the necessary supplies for their "
          "journey on foot. David shifts his body around, mustering up the courage to finally stand up, despite his egregious wounds. ",
          "Continue",
          "Continue",
          61,
          61,
          1))  # 60
scenes.append(
    Scene("He triumphantly stands up, ready to start their journey. He turns around to assist Cole with unloading the car, only to find the ground quickly approaching his face. "
          " David collapses to the ground and blacks out, his future uncertain. ",
          "Continue",
          "Continue",
          62,
          62,
          1))  # 61
scenes.append(
    Scene("Chapter 3: Cole", "Continue", "Continue", 63, 63, 1, True, introMusic)
)  # 62

scenes.append(
    Scene("Cole watches in horror as his father collapses. He runs towards his father, catching him before he hits the ground. The sky continues to darken, as night continues to fall. He has no choice but to drag his body to a safe location for the night. ",
          "Continue",
          "Continue",
          64,
          64,
          1))  # 63
scenes.append(
    Scene("Cole is uncertain of how long his father will remain unchanged. According to the radio, the camp should only be a few miles down the road. He wonders if he should risk"
          " traversing in the road through the night or bunkering down for the night and leaving in the morning. ",
          "Leave now",
          "Wait until morning",
          65,
          66,
          2))  # 64
scenes.append(
    Scene("Cole knows his father needs assistance as soon as possible. He quickly grabs his flashlight, gun, and belongings. "
          "Before he leaves, he leaves him a quick note next to his backpack if David should wake up before his return. ",
          "Continue",
          "Continue",
          67,
          67,
          1))  # 65
scenes.append(
    Scene("Cole knows his best chance at avoiding the zombies is to travel in the sunlight, where he can see any incoming threats. Before he goes to sleep, "
          "he places a strip of duct tape over his father's mouth to hopefully ward off any late night attacks should he turn. ",
          "Continue",
          "Continue",
          67,
          67,
          1))  # 66
scenes.append(
    Scene("With belongings in tow, he sets off on an arduous journey, with no idea what dangers lie ahead. At every sound, Cole jumps in fright, using his flashlight to inspect the potential source of danger. "
          "After hours of walking, with no end in sight, Cole begins to lose hope. Out of the corner of his eye, he spots a large neon sign in the distance. With renewed energy, he heads toward the sign.",
          "Continue",
          "Continue",
          68,
          68,
          1))  # 67
scenes.append(
    Scene("Once Cole gets closer to the sign, he sees a tall chain-link fence encompassing a massive compound. With absolute certainty, he knows that this area is the "
          "survivor's camp. As he gets closer, Cole stops and wonders how he should approach the camp. ",
          "Shout and Scream while Sprinting",
          "Gather intel",
          69,
          70,
          2))  # 68
scenes.append(
    Scene("Cole decides that his best bet to draw attention to himself, which should hopefully alert any guards that he is a human in search of help, rather than a stray zombie. He starts singing and yelling as he gets closer to the camp, and he notices movement from within the walls of the base. ",
          "Continue",
          "Continue",
          71,
          71,
          1))  # 69
scenes.append(
    Scene("Cole decides that his best bet to scope out the base to ensure that the base is full of good-intentioned survivors. He gets ready to flank the base, borrowing knowledge from his handy ninja handbook.",
          "Continue",
          "Continue",
          71,
          71,
          1))  # 70
scenes.append(
    Scene("Suddenly, he hears an engine roar and he turns around to find a military vehicle barreling towards him. He waves and shouts in front of the path of the vehicle, which skids to a stop. The doors open, and two survivors jump out. ",
          "Continue",
          "Continue",
          72,
          72,
          1))  # 71
scenes.append(
    Scene("Cole is beyond relieved to see real people but quickly remembers his father's peril. He rushes over and screams about his father's predicament and pleads to the survivors to help him.",
          "Continue",
          "Continue",
          73,
          73,
          1))  # 72
scenes.append(
    Scene("The survivors, worried to see a child alone in the apocalypse, agree to help, and the trio pile into the vehicle. After a quick drive, Cole spots their car along the road and the group pulls over.",
          "Continue",
          "Continue",
          74,
          74,
          1))  # 73
scenes.append(
    Scene("Cole rushes to his father's resting place and is ecstatic to find him still there. "
          "The survivors, asking no questions, quickly pick up the limp body of David and place him in the back of the truck. As the engine starts up again, Cole is relieved, "
          "and promptly passes out from exhaustion, with their futures uncertain.",
          "Exit Game",
          "Exit Game",
          75,
          75,
          1))  # 74

scenes.append(Scene("Game Over", "Exit Game", "Exit Game", 76, 76, 1))  # 75
scenes.append(Scene("Thank you for playing!", "Exit Game", "Exit Game", 76, 76, 1))  # 76





def showText(text):
    text_box.set_text(text)
    text_box.set_active_effect(
        pygame_gui.TEXT_EFFECT_TYPING_APPEAR,
        params={"time_per_letter": 0.02, "time_per_letter_deviation": 0},
    )


def showImage(scene_text):
    placement_tuple = (272, 230)
    try:
        img_name = "image"
        ig.generate(
            data=f'Zombie apocalypse style, "{scene_text}"',
            input_type="prompt",
            output_name=img_name,
        )
        # Resize image to 256x256
        img = Image.open(f"{images_dir}{img_name}.png")
        img_resized = img.resize((256, 256), resample=Image.ANTIALIAS)
        img_resized.save(f"{images_dir}{img_name}.png")
        # Display image
        screen.blit(pygame.image.load(f"{images_dir}{img_name}.png"), placement_tuple)
    except Exception:
        screen.blit(pygame.image.load("data/images/placeholder.png"), placement_tuple)


def showTextButtons(text, x, y):
    surface = font.render(text, True, text_color)
    screen.blit(surface, (x, y))


# Use this to make a button
def choiceButton(text, x, y, w, h):
    pygame.draw.rect(screen, text_color, (x - 0.2, y - 0.1, w + 2, h + 2))
    mousePos = pygame.mouse.get_pos()
    if x + w > mousePos[0] > x and y + h > mousePos[1] > y:
        pygame.draw.rect(screen, button_hover_color, (x, y, w, h))
    else:
        pygame.draw.rect(screen, button_color, (x, y, w, h))

    text_w, text_h = font.size(text)
    showTextButtons(text, x + ((w - text_w) / 2), y + ((h - text_h) / 2))


# Function used to update all variables related to decisions
def newChoice(sceneNum):
    global food, giveGun, shotgun, medicine, twoPlayer, destination, bitTwice, run, eatFood, useMedicine, keepGun, day
    # Chapter 1
    if sceneNum == 2:
        twoPlayer = True
    if sceneNum == 7:
        giveGun = True
    if sceneNum == 10:
        shotgun = True
        destination = "grocery store"
    if sceneNum == 11:
        food = True
    if sceneNum == 14:
        medicine = True
    if sceneNum == 15 or (sceneNum == 14 and giveGun == True):
        food = False
        medicine = True
    if sceneNum == 18 and (giveGun == True and shotgun == False):
        bitTwice = True
    if sceneNum == 19:
        run = True
    if sceneNum == 19 and giveGun == False:
        bitTwice = True
    if sceneNum == 33:
        keepGun = True
    if sceneNum == 34:
        eatFood = True
    if sceneNum == 35:
        useMedicine = True
    if sceneNum == 66:
        day = True
    if sceneNum == 76:
        pygame.quit()
        sys.exit()


# Checks if the text of the current scene should be updated based on previous decisions,
# otherwise returns the scenes default text
def updateChoice(sceneNum):
    # Chapter 1
    if sceneNum == 3 and twoPlayer == True:
        return "Chapter 1: David\nPlayer 1's turn!"
    if sceneNum == 9 and giveGun == True:
        return "Now without his gun and armed with only a knife, David leaves his home for the first time in months. He carefully makes his way from his neighborhood to the outskirts of the town. He notices the gun store and grocery store both seem safe to check. Which should he search first?"
    if sceneNum == 14 and giveGun == True:
        return "David stumbles back and instinctively reaches for his gun, but finds it missing and realizes he had given it to Cole. Before he can ready himself, the zombie grabs him and ferociously tries to bite at his neck. The contents of David's backpack fall to the floor in the struggle, and David narrowly manages to grab his knife and kill the zombie. He then takes the medicine, but the food he had gathered previously is ruined as the cans burst open and are spread into the filth along the floor."
    if sceneNum == 16 and food == True and medicine == True:
        return "Having gathered food and medicine, David goes to exit the store."
    if sceneNum == 16 and food == True and medicine == False:
        return "Having gathered some food, David goes to exit the store."
    if sceneNum == 16 and food == False and medicine == True:
        return "Having gathered medicine, David goes to exit the store."
    if sceneNum == 16 and shotgun == True:
        return "Having gathered a new gun and some ammo, David goes to exit the store."
    if sceneNum == 17:
        return (
            "David approaches the exit and peaks his head out to survey the surrounding area. The street looks clear, and David heads outside towards the "
            + destination
            + ". Just as he nears his destination he turns a corner and is confronted by two zombies."
        )
    if sceneNum == 18 and bitTwice == True:
        return "With no available gun, David pulls out his knife to defend himself. He tries to take out one of the zombies but the flesh hungry monsters manage to overpower him and tackle him to the ground. David uses all of his strength to hold them back, but things are looking grim."
    if sceneNum == 22 and run == False and bitTwice == True:
        return "Cole follows his fathers path and heads towards the town. He reaches the outskirts when he hears yelling in the distance. He sprints into the town and sees his father struggling with two zombies."
    if sceneNum == 22 and run == False and bitTwice == False:
        return "Cole follows his fathers path and heads towards the town. He reaches the outskirts when he hears yelling in the distance. He sprints into the town and sees his father struggling with a zombie."
    if sceneNum == 23 and run == False and bitTwice == False:
        return "Cole continues to run towards his father to help but before he can get there the zombie sinks its teeth into his fathers arm. Cole screams in horror, and David yells for him to stay back."
    if sceneNum == 23 and run == False and bitTwice == True:
        return "Cole continues to run towards his father to help but before he can get there one zombie sinks its teeth into his fathers arm and the other into his leg. Cole screams in horror, and David yells for him to stay back."
    if sceneNum == 24 and giveGun == False and run == False:
        return "Unarmed and helpless, Cole quickly grabs an old wooden board on the street and runs to his father. He swings at the zombie with all his strength, but it is unaffected and remains focused on David. He finally unleashes a massive swing that stuns the zombie and gives David the chance to grab his knife and kill it for good."
    if sceneNum == 24 and giveGun == True and run == False and bitTwice == False:
        return "Cole takes out the gun his father trusted him with and lines up his target. He fires multiple shots but the zombie is unaffected. Down to his last shot, he fires into the Zombie's head and kills it for good."
    if sceneNum == 24 and giveGun == True and run == False and bitTwice == True:
        return "Cole takes out the gun his father trusted him with and lines up his target. He fires multiple shots but the zombie is unaffected. Down to his last shot, he fires into the Zombie's head and kills it for good. David uses this opportunity to grab his knife and kill the remaining zombie."
    if sceneNum == 24 and run == True and giveGun == False:
        return "Unarmed and helpless, Cole quickly grabs an old wooden board on the street and runs to his father. He desperately tries to hit and distract the zombies but it is no use, as they remain fixated on David. With David's energy spent, David tries to reach for his knife as one zombie sinks its teeth into his leg and the other his arm. He screams in pain and in a burst of adrenaline, uses this momement to kill them as they bite into him."
    if sceneNum == 25 and run == False and bitTwice == False:
        return "Afraid and unsure of what to do, Cole listens to his father and keeps his distance. David gains a burst of adrenaline and uses his free hand to finally grab his knife and kill the zombie for good."
    if sceneNum == 25 and run == False and bitTwice == True:
        return "Afraid and unsure of what to do, Cole listens to his father and keeps his distance. With the zombies now distracted, David gains a burst of adrenaline and gets ahold of his knife and kill both zombies for good."
    if sceneNum == 30 and medicine == True:
        runScene(32)
    if sceneNum == 30 and medicine == False and food == True:
        runScene(31)
    if sceneNum == 74 and day == True:
        return "Cole rushes to his father's resting place and is shocked to find it empty. The note remains untouched and David's bag still remains in the same spot. Cole looks out into the distance, understanding the fate of his father. "    


    return scenes[sceneNum].mainText


# main function that can be given a scene and will handle everything associated with displaying that scene
def runScene(sceneNum):
    if scenes[sceneNum].switchMusic:
        pygame.mixer.fadeout(3000)
        scenes[sceneNum].soundClip.play()

    screen.fill(background_color)
    scene_text = updateChoice(sceneNum)
    showText(scene_text)
    showImage(scene_text)

    time_delta = clock.tick(60) / 1000.0

    buttonWidth = 325
    buttonHeight = 40

    button1X = 50
    button1Y = 530

    button2X = WIDTH - buttonWidth - button1X
    button2Y = button1Y

    if scenes[sceneNum].numButtons == 1:
        button1X = (WIDTH - buttonWidth) // 2

    # manager.process_events(event)
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if (
                        x > button1X
                        and x < (button1X + buttonWidth)
                        and y > button1Y
                        and y < (button1Y + buttonHeight)
                    ):
                        newChoice(scenes[sceneNum].sceneOption1Index)
                        runScene(scenes[sceneNum].sceneOption1Index)
                    elif (
                        x > button2X
                        and x < (button2X + buttonWidth)
                        and y > button2Y
                        and y < (button2Y + buttonHeight)
                        and scenes[sceneNum].numButtons == 2
                    ):
                        newChoice(scenes[sceneNum].sceneOption2Index)
                        runScene(scenes[sceneNum].sceneOption2Index)
            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(window_surface)
        if showTextButtons:
            choiceButton(
                scenes[sceneNum].button1Text,
                button1X,
                button1Y,
                buttonWidth,
                buttonHeight,
            )
            if scenes[sceneNum].numButtons == 2:
                choiceButton(
                    scenes[sceneNum].button2Text,
                    button2X,
                    button2Y,
                    buttonWidth,
                    buttonHeight,
                )
        pygame.display.update()


clock = pygame.time.Clock()
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        manager.process_events(event)

    window_surface.blit(background, (0, 0))

    pygame.display.update()
    time_delta = clock.tick(60) / 1000.0

    manager.update(time_delta)

    manager.draw_ui(window_surface)

    runScene(0)

# Remove temp dir
shutil.rmtree(images_dir)
