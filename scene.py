class Scene:
    """
    Represents a scene in the game.

    Attributes:
        mainText (str): The main text to display in the scene.
        button1Text (str): The text to display on the first button.
        button2Text (str): The text to display on the second button.
        sceneOption1Index (int): The index of the scene to go to if the first button is clicked.
        sceneOption2Index (int): The index of the scene to go to if the second button is clicked.
        numButtons (int): The number of buttons to display in the scene (either 1 or 2).
        switchMusic (bool): Whether or not to switch the background music when the scene is displayed.
        soundClip (pygame.mixer.Sound): The sound clip to play when the scene is displayed.
    """

    def __init__(self, mainText, button1Text, button2Text, sceneOption1Index, sceneOption2Index, numButtons, switchMusic=False, soundClip=None):
        self.mainText = mainText
        self.button1Text = button1Text
        self.button2Text = button2Text
        self.sceneOption1Index = sceneOption1Index
        self.sceneOption2Index = sceneOption2Index
        self.numButtons = numButtons
        self.switchMusic = switchMusic
        self.soundClip = soundClip
