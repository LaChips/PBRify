#!/usr/bin/python

import os
import sys
import shutil
from PIL import Image
import json
import PySimpleGUI as sg
from src.copyPackAndUnzip import copyPackAndUnzip
from src.pbrify import start
from src.initWindow import initWindow
import src.vars as gvars
from multiprocessing import Process
from src.fetchTextures import getTextures
from src.createNormalsMaps import createNormal, createNormals
from src.createHeightMaps import createHeightMap, createHeightMaps
from src.repackTextures import repackTextures
from src.createSpecularMaps import createSpecularMap, createSpecularMaps
from pathlib import Path

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

def displayMaps(texture, textureName):
    diffuse = Image.open(r"" + os.path.join(texture.path, texture.name + texture.ext), 'r', ['png']).convert('RGB')
    size = diffuse.size[0]
    zoom = 128 / size if size <= 128 else 1
    subsample = 1 if size <= 128 else size / 128
    try:
        gvars.second_window['-DIFFUSE-PREVIEW-'].update(filename=(texture.path + textureName + texture.ext), zoom=zoom, subsample=subsample)
    except:
        print("can't load texture " + texture.name)
        return
    try:
        gvars.second_window['-NORMAL-PREVIEW-'].update(filename=(texture.path + textureName + '_n' + texture.ext), zoom=zoom, subsample=subsample)
    except:
        print("can't load texture " + texture.name)
        return
    try:
        gvars.second_window['-HEIGHT-PREVIEW-'].update(filename=(texture.path + textureName + '_h' + texture.ext), zoom=zoom, subsample=subsample)
    except:
        print("can't load texture " + texture.name)
        return
    try:
        gvars.second_window['-SPECULAR-PREVIEW-'].update(filename=(texture.path + textureName + '_s' + texture.ext), zoom=zoom, subsample=subsample)
    except:
        print("can't load texture " + texture.name)
        return
    
def displaySpecularValues(texture, textureName):
    if (textureName not in gvars.textures_data):
        return
    specValues = texture.customValues.copy() if texture.customValues else gvars.textures_data[textureName].copy()
    subValuesList = [specValues[n:n+2] for n in range(0, len(specValues), 2)]
    for i in range(0, len(subValuesList)):
        colorAndSpecularBlock = [[], [], [], []]
        for j in range(0, len(subValuesList[i])):
            specValue = subValuesList[i][j]
            valueIndex = i * 2 + j
            hexColor = '#' + ('{:02X}' * 3).format(specValue['color'][0], specValue['color'][1], specValue['color'][2])
            hexSpecular = '#' + ('{:02X}' * 3).format(specValue['specular'][0], specValue['specular'][1], specValue['specular'][2])
            if gvars.editedTextureName == None:
                colorAndSpecularBlock[0].append(sg.Canvas(size=(120, 50), background_color=hexColor, key='-SINGLE-SPECULAR-COLOR-:' + str(valueIndex)))
                colorAndSpecularBlock[0].append(sg.Canvas(size=(120, 50), background_color=hexSpecular, key='-SINGLE-SPECULAR-SPECULAR-:' + str(valueIndex)))
                colorAndSpecularBlock[1].append(sg.Text("R :", size=(3, 1)))
                colorAndSpecularBlock[1].append(sg.InputText(str(specValue['color'][0]), size=(15, 1), key='-SINGLE-COLOR-RED-EDIT-:' + str(valueIndex), enable_events=True))
                colorAndSpecularBlock[1].append(sg.InputText(str(specValue['specular'][0]), size=(15, 1), key='-SINGLE-SPECULAR-RED-EDIT-:' + str(valueIndex), enable_events=True))
                colorAndSpecularBlock[2].append(sg.Text("G :", size=(3, 1)))
                colorAndSpecularBlock[2].append(sg.InputText(str(specValue['color'][1]), size=(15, 1), key='-SINGLE-COLOR-GREEN-EDIT-:' + str(valueIndex), enable_events=True))
                colorAndSpecularBlock[2].append(sg.InputText(str(specValue['specular'][1]), size=(15, 1), key='-SINGLE-SPECULAR-GREEN-EDIT-:' + str(valueIndex), enable_events=True))
                colorAndSpecularBlock[3].append(sg.Text("B :", size=(3, 1)))
                colorAndSpecularBlock[3].append(sg.InputText(str(specValue['color'][2]), size=(15, 1), key='-SINGLE-COLOR-BLUE-EDIT-:' + str(valueIndex), enable_events=True))
                colorAndSpecularBlock[3].append(sg.InputText(str(specValue['specular'][2]), size=(15, 1), key='-SINGLE-SPECULAR-BLUE-EDIT-:' + str(valueIndex), enable_events=True))
            else:
                gvars.second_window['-SINGLE-SPECULAR-COLOR-:' + str(valueIndex)].update(background_color=hexColor)
                gvars.second_window['-SINGLE-SPECULAR-SPECULAR-:' + str(valueIndex)].update(background_color=hexSpecular)
        if gvars.editedTextureName == None:
            gvars.second_window.extend_layout(gvars.second_window['-SPECULAR-MAP-VALUES-'], colorAndSpecularBlock)
    

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
        indexesToSelect = []
        for block in gvars.blocks_to_ignore_tmp:
            try:
                indexesToSelect.append(gvars.blocks_names.index(block))
            except:
                continue
        gvars.second_window['-FILTER_TEXTURE-'].update(set_to_index=indexesToSelect)
    elif event2 == '-EDIT_TEXTURE-':
        textureName = values2['-EDIT_TEXTURE-'][0].split('/')[1]
        texture = next((x for x in gvars.textures['diffuses'] if x.name == textureName), None)
        if texture == None or textureName == gvars.editedTextureName:
            print("texture not found")
            return
        displayMaps(texture,  texture.name)
        displaySpecularValues(texture, texture.name)
        texturesValues = gvars.textures_data[texture.name]
        texture.customValues = texturesValues
        gvars.editedTexture = texture
        gvars.editedTextureName = texture.name
    elif event2 == '-INVERT-NORMAL-RED-':
        gvars.editedTexture.reversedNormalsRed = values2['-INVERT-NORMAL-RED-']
    elif event2 == '-INVERT-NORMAL-GREEN-':
        gvars.editedTexture.reversedNormalsGreen = values2['-INVERT-NORMAL-GREEN-']
    elif event2 == '-INVERT-NORMAL-HEIGHT-':
        gvars.editedTexture.reversedNormalsHeight = values2['-INVERT-NORMAL-HEIGHT-']
    elif event2 == '-INVERT-HEIGHT-':
        gvars.editedTexture.reversedHeight = values2['-INVERT-HEIGHT-']
    elif event2 == '-SINGLE-NORMAL-':
        gvars.editedTexture.normalIntensity = values2['-SINGLE-NORMAL-']
    elif event2 == '-SINGLE-HEIGHT-':
        gvars.editedTexture.heightIntensity = values2['-SINGLE-HEIGHT-']
    elif event2 == '-SINGLE-HEIGHT-BRIGHTNESS-':
        gvars.editedTexture.heightBrightness = values2['-SINGLE-HEIGHT-BRIGHTNESS-']
    elif event2.split(':')[0] == '-SINGLE-SPECULAR-RED-EDIT-':
        try:
            value = int(values2[event2])
            gvars.editedTexture.customValues[int(event2.split(':')[1])]['specular'][0] = value
            gvars.second_window['-SINGLE-SPECULAR-SPECULAR-:' + event2.split(':')[1]].update(background_color='#' + ('{:02X}' * 3).format(value, gvars.editedTexture.customValues[int(event2.split(':')[1])]['specular'][1], gvars.editedTexture.customValues[int(event2.split(':')[1])]['specular'][2]))
        except:
            return
    elif event2.split(':')[0] == '-SINGLE-SPECULAR-GREEN-EDIT-':
        try:
            value = int(values2[event2])
            gvars.editedTexture.customValues[int(event2.split(':')[1])]['specular'][1] = value
            gvars.second_window['-SINGLE-SPECULAR-SPECULAR-:' + event2.split(':')[1]].update(background_color='#' + ('{:02X}' * 3).format(gvars.editedTexture.customValues[int(event2.split(':')[1])]['specular'][0], value, gvars.editedTexture.customValues[int(event2.split(':')[1])]['specular'][2]))
        except:
            return
    elif event2.split(':')[0] == '-SINGLE-SPECULAR-BLUE-EDIT-':
        try:
            value = int(values2[event2])
            gvars.editedTexture.customValues[int(event2.split(':')[1])]['specular'][2] = value
            gvars.second_window['-SINGLE-SPECULAR-SPECULAR-:' + event2.split(':')[1]].update(background_color='#' + ('{:02X}' * 3).format(gvars.editedTexture.customValues[int(event2.split(':')[1])]['specular'][0], gvars.editedTexture.customValues[int(event2.split(':')[1])]['specular'][1], value))
        except:
            return
    elif event2.split(':')[0] == '-SINGLE-COLOR-RED-EDIT-':
        try:
            value = int(values2[event2])
            gvars.editedTexture.customValues[int(event2.split(':')[1])]['color'][0] = value
            gvars.second_window['-SINGLE-SPECULAR-COLOR-:' + event2.split(':')[1]].update(background_color='#' + ('{:02X}' * 3).format(value, gvars.editedTexture.customValues[int(event2.split(':')[1])]['color'][1], gvars.editedTexture.customValues[int(event2.split(':')[1])]['color'][2]))
        except:
            return
    elif event2.split(':')[0] == '-SINGLE-COLOR-GREEN-EDIT-':
        try:
            value = int(values2[event2])
            gvars.second_window['-SINGLE-SPECULAR-COLOR-:' + event2.split(':')[1]].update(background_color='#' + ('{:02X}' * 3).format(gvars.editedTexture.customValues[int(event2.split(':')[1])]['color'][0], value, gvars.editedTexture.customValues[int(event2.split(':')[1])]['color'][2]))
            gvars.editedTexture.customValues[int(event2.split(':')[1])]['color'][1] = value
        except:
            return
    elif event2.split(':')[0] == '-SINGLE-COLOR-BLUE-EDIT-':
        try:
            value = int(values2[event2])
            gvars.editedTexture.customValues[int(event2.split(':')[1])]['color'][2] = value
            gvars.second_window['-SINGLE-SPECULAR-COLOR-:' + event2.split(':')[1]].update(background_color='#' + ('{:02X}' * 3).format(gvars.editedTexture.customValues[int(event2.split(':')[1])]['color'][0], gvars.editedTexture.customValues[int(event2.split(':')[1])]['color'][1], value))
        except:
            return
    elif event2 == '-CONVERT-TEXTURE-':
        createSpecularMap(gvars.editedTexture)


def handleBlockProcess(event, values):
    if event[0] == '-SPECULAR-GENERATION-':
        gvars.window['progress'].update(int(event[1].split(':')[1]) + 1, len(gvars.textures['speculars']))
        gvars.window['state'].update(value="Generating specular maps for " + event[1].split(':')[0])
    elif event[0] == '-NORMAL-GENERATION-':
        gvars.window['progress'].update(int(event[1].split(':')[1]) + 1, len(gvars.textures['normals']))
        gvars.window['state'].update(value="Generating normal maps for " + event[1].split(':')[0])
    elif event[0] == '-HEIGHT-GENERATION-':
        gvars.window['progress'].update(int(event[1].split(':')[1]) + 1, len(gvars.textures['normals']))
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
        gvars.done = True
        gvars.generation_done = True
    elif event[1] == '-SINGLE-SPECULAR-THREAD-ENDED-':
        createNormal(gvars.editedTexture)
    elif event[1] == '-SINGLE-NORMAL-THREAD-ENDED-':
        createHeightMap(gvars.editedTexture)
    elif event[1] == '-SINGLE-HEIGHT-THREAD-ENDED-':
        displayMaps(gvars.editedTexture,  gvars.editedTextureName)
        #displaySpecularValues(gvars.editedTexture,  gvars.editedTextureName)

if __name__ == '__main__':
    main()