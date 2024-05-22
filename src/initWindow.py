import os
import PySimpleGUI as sg
from PySimpleGUI import FileBrowse, ProgressBar, Slider
from src.fetchTextures import getTextures
import src.vars as gvars
import json

def pluck(lst, key):
    return [x.__getattribute__(key) for x in lst]

def initWindow(screen):
    layout = []
    if (screen == 'main'):
        layout = [
            [sg.Text('Resource pack   '), sg.In(size=(50,1), enable_events=True ,key='-PACK-'), sg.FileBrowse(key='pack_path')],
            [sg.Text('Output directory '), sg.In(size=(50,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Text('Normal strenght  '), sg.Slider(size=(50, 10), default_value=1, range=(1, 3), resolution=0.001, orientation='h', enable_events=True, key='-NORMAL-')],
            [sg.Text('Height strenght   '), sg.Slider(size=(50, 10), default_value=0.12, range=(0.01, 0.5), resolution=0.001, orientation='h', enable_events=True, key='-HEIGHT-')],
            [sg.Checkbox('Fast specular map generation (less accurate) ', default=False, enable_events=True, key='-FAST-')],
            [sg.Button('Exclude blocks', key='-FILTER_TEXTURES-', visible=False)],
            [sg.Text(text='', size=(50,1), key='state', visible=False)],
            [sg.ProgressBar(size=(50,5), max_value=0, key='progress', orientation='horizontal', visible=False)],
            [sg.Button('Convert', key='-CONVERT-'), sg.Button('Cancel', key='-CANCEL-'), sg.Button('Export', key='-EXPORT-', visible=False), sg.Button('Edit textures', key='-EDIT-', visible=False)] # TO CHANGE!!!!
        ]
        return sg.Window('PBRify', layout)
    elif (screen == 'filterTextures'):
        layout = [
            [sg.Text('Select the textures to exclude')],
            [sg.Button('Unselect all', key='-FILTER_TEXTURES-NONE-'), sg.Button('Select plants', key='-FILTER_TEXTURES-PLANT-')],
        ]
        #with open(os.path.join(gvars.base_path, 'lib/textures_data.json'), 'r') as json_file:
            # textures_data = json.loads(json_file.read())
            # blocks_names = list(textures_data.keys())
        textures = getTextures()
        blocks_names = pluck(textures['diffuses'], 'name')
        blocks_path = pluck(textures['diffuses'], 'path')
        names_with_path = [blocks_path[i].split(os.path.join(gvars.base_path, os.path.join('pack_unziped', 'assets', 'minecraft', 'textures')))[1] + blocks_names[i] for i in range(0, len(blocks_names))]
        layout.append([sg.Listbox(names_with_path, size=(200, 30), enable_events=True, select_mode=sg.SELECT_MODE_MULTIPLE, key='-FILTER_TEXTURE-', default_values=gvars.blocks_to_ignore)])
        gvars.blocks_names = names_with_path
            
        layout.append([sg.Button('Confirm', key='-MAIN-')])
        return sg.Window('PBRify - Exclude blocks', layout)
    elif (screen == 'editTextures'):
        layout = [
            [sg.Text('Select the textures to edit (not implemented yet)')],
        ]
        texturesWithoutIgnored = [x for x in gvars.textures['diffuses'] if x.name not in gvars.blocks_to_ignore]
        textures_names = pluck(texturesWithoutIgnored, 'name')
        blocks_path = pluck(texturesWithoutIgnored, 'path')
        names_with_path = [blocks_path[i].split(os.path.join(gvars.base_path, os.path.join('pack_unziped', 'assets', 'minecraft', 'textures')))[1] + textures_names[i] for i in range(0, len(textures_names))]
        imagesLayout= [
            [
                sg.Image(filename=(os.path.join(gvars.base_path, 'src', 'assets', 'diffuse_placeholder.png')), key='-DIFFUSE-PREVIEW-'),
                sg.Image(filename=(os.path.join(gvars.base_path, 'src', 'assets', 'normal_placeholder.png')), key='-NORMAL-PREVIEW-'),
                sg.Image(filename=(os.path.join(gvars.base_path, 'src', 'assets', 'height_placeholder.png')), key='-HEIGHT-PREVIEW-'),
                sg.Image(filename=(os.path.join(gvars.base_path, 'src', 'assets', 'specular_placeholder.png')), key='-SPECULAR-PREVIEW-')
            ]
        ]
        editLayout = [
            [sg.Frame('Textures', imagesLayout)],
            [sg.Checkbox('Invert normals red ', default=False, enable_events=True, key='-INVERT-NORMAL-RED-')],
            [sg.Checkbox('Invert normals green ', default=False, enable_events=True, key='-INVERT-NORMAL-GREEN-')],
            [sg.Checkbox('Invert normals height ', default=False, enable_events=True, key='-INVERT-NORMAL-HEIGHT-')],
            [sg.Checkbox('Invert height displacement ', default=False, enable_events=True, key='-INVERT-HEIGHT-')],
            [sg.Text('Normal strenght  '), sg.Slider(size=(50, 10), default_value=1, range=(1, 3), resolution=0.001, orientation='h', enable_events=True, key='-SINGLE-NORMAL-')],
            [sg.Text('Height strenght   '), sg.Slider(size=(50, 10), default_value=0.12, range=(0.01, 0.5), resolution=0.001, orientation='h', enable_events=True, key='-SINGLE-HEIGHT-')],
            [sg.Text('Height brightness '), sg.Slider(size=(50, 10), default_value=1, range=(0.01, 3), resolution=0.001, orientation='h', enable_events=True, key='-SINGLE-HEIGHT-BRIGHTNESS-')],
            [sg.Checkbox('Fast specular map generation (less accurate) ', default=False, enable_events=True, key='-FAST-')],
            [sg.Col([], key='-SPECULAR-MAP-VALUES-')],
            [sg.Button('Recompute', key='-CONVERT-TEXTURE-')]
        ]

        layout.append([sg.Listbox(names_with_path, size=(100, 30), enable_events=True, key='-EDIT_TEXTURE-'), sg.Frame('Edit texture', editLayout)])
        layout.append([sg.Button('Confirm', key='-MAIN-')])
        return sg.Window('PBRify - Edit generation', layout)
