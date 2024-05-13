import os
import PySimpleGUI as sg
from PySimpleGUI import FileBrowse, ProgressBar, Slider
from src.fetchTextures import getTextures
import src.vars as gvars
import json

def initWindow(screen):
    layout = []
    if (screen == 'main'):
        layout = [
            [sg.Text('Resource pack   '), sg.In(size=(50,1), enable_events=True ,key='-PACK-'), sg.FileBrowse(key='pack_path')],
            [sg.Text('Output directory '), sg.In(size=(50,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Text('Normal strenght  '), sg.Slider(size=(50, 10), default_value=1, range=(1, 3), resolution=0.001, orientation='h', enable_events=True, key='-NORMAL-')],
            [sg.Text('Height strenght   '), sg.Slider(size=(50, 10), default_value=0.12, range=(0.01, 0.5), resolution=0.001, orientation='h', enable_events=True, key='-HEIGHT-')],
            [sg.Checkbox('Fast specular map generation (less accurate) ', default=False, enable_events=True, key='-FAST-')],
            [sg.Button('Exclude blocks', key='-FILTER_TEXTURES-')],
            [sg.Text(text='', size=(50,1), key='state', visible=False)],
            [sg.ProgressBar(size=(50,5), max_value=0, key='progress', orientation='horizontal', visible=False)],
            [sg.Button('Convert', key='-CONVERT-'), sg.Button('Cancel', key='-CANCEL-'), sg.Button('Exit', key='-EXIT-', visible=False)]
        ]
        return sg.Window('PBRify', layout)
    elif (screen == 'filterTextures'):
        layout = [
            [sg.Text('Excluded textures:')],
            [sg.Button('Unselect all', key='-FILTER_TEXTURES-NONE-'), sg.Button('Select plants', key='-FILTER_TEXTURES-PLANT-')],
        ]
        with open(os.path.join(gvars.base_path, 'lib/textures_data.json'), 'r') as json_file:
            textures_data = json.loads(json_file.read())
            blocks_names = list(textures_data.keys())
            layout.append([sg.Listbox(blocks_names, size=(200, 30), enable_events=True, select_mode=sg.SELECT_MODE_MULTIPLE, key='-FILTER_TEXTURE-', default_values=gvars.blocks_to_ignore)])
            gvars.blocks_names = blocks_names
            
        layout.append([sg.Button('Confirm', key='-MAIN-')])
        return sg.Window('PBRify - Exclude blocks', layout)
