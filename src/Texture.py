from typing import Any


class texture: 
    def __init__(self, path, name, ext):
        self.name = name 
        self.path = path 
        self.ext = ext
        self.normalIntensity = None
        self.heightIntensity = None
        self.reversedNormalsRed = None
        self.reversedNormalsGreen = None
        self.reversedHeight = None
        self.fastSpecular = None
        self.heightBrightness = None
        self.customValues = None