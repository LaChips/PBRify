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
from src.fetchTextures import getTextures, listTextures
from src.createNormalsMaps import createNormals
from src.createHeightMaps import createHeightMaps
from src.repackTextures import repackTextures
from src.createSpecularMaps import createSpecularMaps

def main():
    try:
        gvars.base_path = sys._MEIPASS
    except Exception:
        gvars.base_path = os.path.abspath(".")
    gvars.window = initWindow('main')
    with open('./lib/normals_to_convert.json', 'r') as normalsToConvertRaw:
        gvars.normals = json.load(normalsToConvertRaw)
    with open('./lib/speculars_to_convert.json', 'r') as specularsToConvertRaw:
        gvars.speculars = json.load(specularsToConvertRaw)
    while True:
        event, values = gvars.window.read(timeout=0)
        if event != '__TIMEOUT__':
            print("event :", event)
        if event == '-EXIT-' or event == sg.WIN_CLOSED:
            break
        handleMainWindowEvents(event, values)
        handleSecondWindowEvents()
        handleBlockProcess(event, values)
        handleThreadsEvent(event, values)
        if gvars.done == True:
            gvars.done = False
            os.remove(os.path.join(gvars.base_path, 'pack.zip'))
            shutil.rmtree(os.path.join(gvars.base_path, 'pack_unziped'), ignore_errors=True)
            gvars.window['state'].update(value="Done!")
            gvars.window['-CONVERT-'].update(visible=False)
            gvars.window['-CANCEL-'].update(visible=False)
            gvars.window['-EXIT-'].update(visible=True)
    gvars.window.close()

def handleSecondWindowEvents():
    event2, values2 = (None, None)
    if (gvars.second_window != None):
        event2, values2 = gvars.second_window.read(timeout=0)
    if (event2 == None):
        return
    if event2 == '-MAIN-':
        gvars.blocks_to_ignore = gvars.blocks_to_ignore_tmp
        gvars.second_window.close()
    elif event2 == '-FILTER_TEXTURE-':
        gvars.blocks_to_ignore_tmp = values2['-FILTER_TEXTURE-']
    elif event2 == '-FILTER_TEXTURES-NONE-':
        gvars.blocks_to_ignore_tmp = []
        gvars.second_window['-FILTER_TEXTURE-'].update(set_to_index=[])
    elif event2 == '-FILTER_TEXTURES-PLANT-':
        gvars.blocks_to_ignore_tmp = gvars.blocks_to_ignore_tmp + gvars.plant_blocks
        gvars.second_window['-FILTER_TEXTURE-'].update(set_to_index=[gvars.blocks_names.index(block) for block in gvars.blocks_to_ignore_tmp])

def handleMainWindowEvents(event, values):
    if event == '-FILTER_TEXTURES-':
        gvars.second_window = initWindow('filterTextures')
    elif event == '-FOLDER-':
        gvars.directory = values['-FOLDER-']
    elif event == "-PACK-":
        if (values):
            gvars.pack = values['-PACK-']
    elif event == "-NORMAL-":
        gvars.normalIntensity = values['-NORMAL-']
    elif event == "-HEIGHT-":
        gvars.heightIntensity = values['-HEIGHT-']
    elif event == "-FAST-":
        gvars.fastSpecular = values['-FAST-']
    elif event == "-CONVERT-" and gvars.pack != None and gvars.directory != None:
        start()
        gvars.done = False
        gvars.generation_done = False
        textures = getTextures()
        gvars.textures = textures
        gvars.window['state'].update(value="Generating specular maps")
        createSpecularMaps(textures['speculars'])

def handleBlockProcess(event, values):
    if event[0] == '-SPECULAR-GENERATION-':
        gvars.window['progress'].update(int(event[1].split(':')[1]) + 1, len(gvars.textures['speculars']))
        gvars.window['state'].update(value="Generating specular maps for " + event[1].split(':')[0])
    elif event[0] == '-NORMAL-GENERATION-':
        gvars.window['progress'].update(int(event[1].split(':')[1]) + 1, len(gvars.textures))
        gvars.window['state'].update(value="Generating normal maps for " + event[1].split(':')[0])
    elif event[0] == '-HEIGHT-GENERATION-':
        gvars.window['progress'].update(int(event[1].split(':')[1]) + 1, len(gvars.textures))
        gvars.window['state'].update(value="Generating height maps for " + event[1].split(':')[0])

def handleThreadsEvent(event, values):
    if event[1] == '-SPECULAR-THREAD-ENDED-':
        print("SPECULAR THREAD ENDED")
        gvars.window['state'].update(value="Generating normals maps")
        createNormals(gvars.textures['normals'])
    elif event[1] == '-NORMAL-THREAD-ENDED-':
        print("NORMAL THREAD ENDED")
        gvars.window['state'].update(value="Generating height maps")
        createHeightMaps(gvars.textures['normals'])
    elif event[1] == '-HEIGHT-THREAD-ENDED-':
        if (gvars.generation_done == True):
            return
        print("HEIGHT THREAD ENDED")
        gvars.window['state'].update(value="Repacking textures")
        repackTextures(gvars.pack.split('/')[len(gvars.pack.split('/')) - 1].split('.zip')[0] + "_PBR_" +  "fast" if gvars.fastSpecular else "slow")
        gvars.done = True
        gvars.generation_done = True

if __name__ == '__main__':
    main()