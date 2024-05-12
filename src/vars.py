import PySimpleGUI as sg

UNZIP_DIR = 'pack_unzipped'

class AppState:
    def __init__(self):
        self.window : sg.Window = None
        self.done = False

    def updateStateText(self, new_state = 'invalid state'):
        if self.window is not None:
            self.window['state'].update(value=new_state)

    def updateProgressBar(self, current = 0, end = 1):
        if self.window is not None:
            self.window['progress'].update(current, end)

    def setState(self, started : bool):
        if self.window is not None:
            self.window['state'].update(visible=started)
            self.window['progress'].update(visible=started)

class Config:
    def __init__(self) -> None:
        self.directory = None
        self.pack = None
        self.base_path = None
        self.normalIntensity = 1
        self.heightIntensity = 0.1
        self.fastSpecular = False
        self.normals = []
        self.speculars = []