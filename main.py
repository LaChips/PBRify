#!/usr/bin/python

import os
import sys
import shutil
import scipy.ndimage
from scipy import ndimage
import json
import argparse
from PySimpleGUI import FileBrowse, ProgressBar
from src.pbrify import Converter
from src.initWindow import initWindow
from src.vars import Config, AppState
from threading import Thread


def main():

    config = Config()
    app = AppState()
    converter = None

    try:
        config.base_path = sys._MEIPASS
    except Exception:
        config.base_path = os.path.abspath(".")

    app.window = initWindow()
    app.window.close_destroys_window = True

    with open('./lib/normals_to_convert.json', 'r') as normalsToConvertRaw:
        config.normals = json.load(normalsToConvertRaw)

    with open('./lib/speculars_to_convert.json', 'r') as specularsToConvertRaw:
        config.speculars = json.load(specularsToConvertRaw)

    while app.window is not None:
        event, values = app.window.read(timeout=0)

        # If the window is closed, close the app
        if event is None:
            break

        if event == 'Cancel':
            app.window.close()

        elif event == '-FOLDER-':
           config.directory = values['-FOLDER-']

        elif event == "-PACK-":
           config.pack = values['-PACK-']

        elif event == "-NORMAL-":
            config.normalIntensity = values['-NORMAL-']

        elif event == "-HEIGHT-":
            config.heightIntensity = values['-HEIGHT-']

        elif event == "-FAST-":
            config.fastSpecular = values['-FAST-']

        elif event == "-CONVERT-" and config.pack != None and config.directory != None:
            # Initialize a new conversion process
            converter = Converter(config, app)
            converter.start()

        elif event == '-EXIT-':
            app.window.close()

        elif app.done == True:
            app.done = False
            os.remove(os.path.join(config.base_path, 'pack.zip'))
            shutil.rmtree(os.path.join(config.base_path, 'pack_unziped'), ignore_errors=True)
            app.window['state'].update(value="Done!")
            app.window['-CONVERT-'].update(visible=False)
            app.window['-CANCEL-'].update(visible=False)
            app.window['-EXIT-'].update(visible=True)


if __name__ == '__main__':
    main()