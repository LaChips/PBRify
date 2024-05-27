from typing import Any


class texture: 
    def __init__(self, path, name, ext):
        self.name = name 
        self.path = path 
        self.ext = ext
        self.normalIntensity = 0
        self.heightIntensity = 0
        self.reversedNormalsRed = None
        self.reversedNormalsGreen = None
        self.reversedHeight = None
        self.fastSpecular = None
        self.heightBrightness = 0
        self.customValues = None