from typing import Any


class texture: 
    def __init__(self, path, name, ext):
        self.name = name 
        self.path = path 
        self.ext = ext
        self.normalIntensity = 0
        self.heightIntensity = 0
        self.reversedNormalsRed = False
        self.reversedNormalsGreen = False
        self.reversedNormalsHeight = False
        self.reversedHeight = False
        self.fastSpecular = False
        self.heightBrightness = 0
        self.customValues = None