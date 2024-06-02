#!/usr/bin/python
import os
import sys
import shutil
import PySimpleGUI as sg
from src.blockProcess import handleBlockProcess
from src.mainWindowEvents import handleMainWindowEvents
from src.secondWindowEvents import handleSecondWindowEvents
from src.initWindow import initWindow
import src.vars as gvars
from src.threadEvents import handleThreadsEvent

def main():
    try:
        gvars.base_path = sys._MEIPASS
    except Exception:
        gvars.base_path = os.path.abspath(".")
    gvars.window = initWindow('main')
    # with open('./lib/normals_to_convert.json', 'r') as normalsToConvertRaw:
    #     gvars.normals = json.load(normalsToConvertRaw)
    # with open('./lib/speculars_to_convert.json', 'r') as specularsToConvertRaw:
    #     gvars.speculars = json.load(specularsToConvertRaw)
    while True:
        event, values = gvars.window.read(timeout=0)
        if event != '__TIMEOUT__':
            print("event :", event)
        if event == sg.WIN_CLOSED:
            os.remove(os.path.join(gvars.base_path, 'pack.zip'))
            shutil.rmtree(os.path.join(gvars.base_path, 'pack_unziped'), ignore_errors=True)
            break
        handleMainWindowEvents(event, values)
        handleSecondWindowEvents()
        handleBlockProcess(event, values)
        handleThreadsEvent(event, values)
        if gvars.done == True:
            gvars.done = False
            gvars.window['state'].update(value="Done! You can now save the pack by clicking on 'Export'. You can also edit it by clicking on 'Edit textures'")
            gvars.window['-CONVERT-'].update(visible=False)
            gvars.window['-CANCEL-'].update(visible=False)
            gvars.window['-EXPORT-'].update(visible=True)
            gvars.window['-EDIT-'].update(visible=True)
    gvars.window.close()

if __name__ == '__main__':
    main()