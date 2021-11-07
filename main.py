#!/usr/bin/python

import os
import scipy.ndimage
from scipy import ndimage
import argparse
import PySimpleGUI as sg
from PySimpleGUI import FileBrowse, ProgressBar
from src.pbrify import start
from src.initWindow import initWindow

window = None
directory = None
pack = None
base_path = os.path.abspath(".")

def main():
    print("base_path :", base_path)
    window = initWindow()
    while True:
        event, values = window.read(timeout=0)
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == '-FOLDER-':
            directory = values['-FOLDER-']
        if event == "-PACK-":
            pack = values['-PACK-']
        if event == "Convert" and pack != None and directory != None:
            start(window, pack, directory, base_path)
    window.close()

if __name__ == '__main__':
    main()