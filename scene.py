class Scene:
    def __init__(self, mainText, button1Text, button2Text, sceneOption1Index, sceneOption2Index, numButtons, switchMusic=False, soundClip=None):
        self.mainText = mainText
        self.button1Text = button1Text
        self.button2Text = button2Text
        self.sceneOption1Index = sceneOption1Index
        self.sceneOption2Index = sceneOption2Index
        self.numButtons = numButtons
        self.switchMusic = switchMusic
        self.soundClip = soundClip
