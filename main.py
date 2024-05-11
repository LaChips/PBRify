#!/usr/bin/python

import os
import sys
import shutil
import scipy.ndimage
from scipy import ndimage
import json
import argparse
import PySimpleGUI as sg
from PySimpleGUI import FileBrowse, ProgressBar
from src.pbrify import start
from src.initWindow import initWindow
import src.vars as gvars
from multiprocessing import Process

def main():
    try:
        gvars.base_path = sys._MEIPASS
    except Exception:
        gvars.base_path = os.path.abspath(".")
    gvars.window = initWindow()
    with open('./lib/normals_to_convert.json', 'r') as normalsToConvertRaw:
        gvars.normals = json.load(normalsToConvertRaw)
    with open('./lib/speculars_to_convert.json', 'r') as specularsToConvertRaw:
        gvars.speculars = json.load(specularsToConvertRaw)
    while True:
        event, values = gvars.window.read(timeout=0)
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        elif event == '-FOLDER-':
           gvars.directory = values['-FOLDER-']
        elif event == "-PACK-":
           gvars.pack = values['-PACK-']
        elif event == "-NORMAL-":
            gvars.normalIntensity = values['-NORMAL-']
        elif event == "-HEIGHT-":
            gvars.heightIntensity = values['-HEIGHT-']
        elif event == "-FAST-":
            gvars.fastSpecular = values['-FAST-']
        elif event == "-CONVERT-" and gvars.pack != None and gvars.directory != None:
            start()
        elif event == '-EXIT-':
            break
        elif gvars.done == True:
            gvars.done = False
            os.remove(os.path.join(gvars.base_path, 'pack.zip'))
            shutil.rmtree(os.path.join(gvars.base_path, 'pack_unziped'), ignore_errors=True)
            gvars.window['state'].update(value="Done!")
            gvars.window['-CONVERT-'].update(visible=False)
            gvars.window['-CANCEL-'].update(visible=False)
            gvars.window['-EXIT-'].update(visible=True)
    gvars.window.close()

if __name__ == '__main__':
    main()