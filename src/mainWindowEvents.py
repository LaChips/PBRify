from src.copyPackAndUnzip import copyPackAndUnzip
from src.createSpecularMaps import createSpecularMaps
from src.fetchTextures import getTextures
from src.initWindow import initWindow
from src.pbrify import start
from src.repackTextures import repackTextures
import src.vars as gvars
import os
import shutil

def handleMainWindowEvents(event, values):
    if event == '-FILTER_TEXTURES-':
        gvars.second_window = initWindow('filterTextures')
    elif event == '-EDIT-':
        gvars.second_window = initWindow('editTextures')
    elif event == '-FOLDER-':
        gvars.directory = values['-FOLDER-']
    elif event == "-PACK-":
        if (values['-PACK-'] != gvars.pack and values['-PACK-'] != None and values['-PACK-'] != ""):
            gvars.pack = values['-PACK-']
            try:
                if (os.path.isfile(os.path.join(gvars.base_path, 'pack.zip'))):
                    os.remove(os.path.join(gvars.base_path, 'pack.zip'))
                if (os.path.isdir(os.path.join(gvars.base_path, 'pack_unziped'))):
                    shutil.rmtree(os.path.join(gvars.base_path, 'pack_unziped'), ignore_errors=True)
                copyPackAndUnzip()
            except Exception as e:
                print("can't copy pack and unzip it : " + str(e))
                return
            gvars.window['-FILTER_TEXTURES-'].update(visible=True)
    elif event == "-NORMAL-":
        gvars.normalIntensity = values['-NORMAL-']
    elif event == "-HEIGHT-":
        gvars.heightIntensity = values['-HEIGHT-']
    elif event == "-FAST-":
        gvars.fastSpecular = values['-FAST-']
    elif event == "-EXPORT-":
        repackTextures(gvars.pack.split('/')[len(gvars.pack.split('/')) - 1].split('.zip')[0] + "_PBR_" +  "fast" if gvars.fastSpecular else "slow")
        gvars.window['state'].update(value="Done")
    elif event == "-CONVERT-" and gvars.pack != None and gvars.directory != None:
        start()
        gvars.done = False
        gvars.generation_done = False
        textures = getTextures()
        gvars.textures = textures
        gvars.window['state'].update(value="Generating specular maps")
        createSpecularMaps(textures['speculars'])
