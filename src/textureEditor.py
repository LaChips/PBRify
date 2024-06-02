import src.vars as gvars
from PIL import Image
import os
import PySimpleGUI as sg

def displayMaps(texture, textureName):
    diffuse = Image.open(r"" + os.path.join(texture.path, texture.name + texture.ext), 'r', ['png']).convert('RGB')
    size = diffuse.size[0]
    zoom = 128 / size if size <= 128 else 1
    subsample = 1 if size <= 128 else size / 128
    gvars.second_window['-DIFFUSE-PREVIEW-'].update(filename=(texture.path + textureName + texture.ext), zoom=zoom, subsample=subsample)
    if (os.path.isfile(os.path.join(texture.path, texture.name + '_n' + texture.ext)) == True):
        gvars.second_window['-NORMAL-PREVIEW-'].update(filename=(texture.path + textureName + '_n' + texture.ext), zoom=zoom, subsample=subsample)
    else:
        gvars.second_window['-NORMAL-PREVIEW-'].update(filename=(os.path.join(gvars.base_path, 'src', 'assets', 'normal_placeholder.png')))
    if (os.path.isfile(os.path.join(texture.path, texture.name + '_h' + texture.ext)) == True):
        gvars.second_window['-HEIGHT-PREVIEW-'].update(filename=(texture.path + textureName + '_h' + texture.ext), zoom=zoom, subsample=subsample)
    else:
        gvars.second_window['-HEIGHT-PREVIEW-'].update(filename=(os.path.join(gvars.base_path, 'src', 'assets', 'height_placeholder.png')))
    if (os.path.isfile(os.path.join(texture.path, texture.name + '_s' + texture.ext)) == True):
        gvars.second_window['-SPECULAR-PREVIEW-'].update(filename=(texture.path + textureName + '_s' + texture.ext), zoom=zoom, subsample=subsample)
    else:
        gvars.second_window['-SPECULAR-PREVIEW-'].update(filename=(os.path.join(gvars.base_path, 'src', 'assets', 'specular_placeholder.png')))
    
def displaySpecularValues(texture, textureName): # Would be way easier if we could clear the values layout and recreate it, but PySimpleGUI doesn't allow it
    if (textureName not in gvars.textures_data):
        return
    specValues = texture.customValues.copy() if texture.customValues else gvars.textures_data[textureName].copy()
    specValuesAmount = len(specValues)
    subValuesList = [specValues[n:n+2] for n in range(0, specValuesAmount, 2)]
    for i in range(0, len(subValuesList)):
        colorAndSpecularBlock = [[], [], [], []]
        for j in range(0, len(subValuesList[i])):
            specValue = subValuesList[i][j]
            valueIndex = i * 2 + j
            hexColor = '#' + ('{:02X}' * 3).format(specValue['color'][0], specValue['color'][1], specValue['color'][2])
            hexSpecular = '#' + ('{:02X}' * 3).format(specValue['specular'][0], specValue['specular'][1], specValue['specular'][2])
            if gvars.editedTextureName == None or valueIndex >= gvars.maxSpecularValuesAmount: # if first edition or texture has more values than the max amount of values from previous editions, we create layout elements
                colorAndSpecularBlock[0].append(sg.Canvas(size=(120, 50), background_color=hexColor, key='-SINGLE-SPECULAR-COLOR-:' + str(valueIndex)))
                colorAndSpecularBlock[0].append(sg.Canvas(size=(120, 50), background_color=hexSpecular, key='-SINGLE-SPECULAR-SPECULAR-:' + str(valueIndex)))
                colorAndSpecularBlock[1].append(sg.Text("R :", size=(3, 1), key='-SINGLE-COLOR-RED-TEXT-:' + str(valueIndex)))
                colorAndSpecularBlock[1].append(sg.InputText(str(specValue['color'][0]), size=(15, 1), key='-SINGLE-COLOR-EDIT-:' + str(valueIndex) + ':RED', enable_events=True))
                colorAndSpecularBlock[1].append(sg.InputText(str(specValue['specular'][0]), size=(15, 1), key='-SINGLE-SPECULAR-EDIT-:' + str(valueIndex) + ':RED', enable_events=True))
                colorAndSpecularBlock[2].append(sg.Text("G :", size=(3, 1), key='-SINGLE-COLOR-GREEN-TEXT-:' + str(valueIndex)))
                colorAndSpecularBlock[2].append(sg.InputText(str(specValue['color'][1]), size=(15, 1), key='-SINGLE-COLOR-EDIT-:' + str(valueIndex) + ':GREEN', enable_events=True))
                colorAndSpecularBlock[2].append(sg.InputText(str(specValue['specular'][1]), size=(15, 1), key='-SINGLE-SPECULAR-EDIT-:' + str(valueIndex) + ':GREEN', enable_events=True))
                colorAndSpecularBlock[3].append(sg.Text("B :", size=(3, 1), key='-SINGLE-COLOR-BLUE-TEXT-:' + str(valueIndex)))
                colorAndSpecularBlock[3].append(sg.InputText(str(specValue['color'][2]), size=(15, 1), key='-SINGLE-COLOR-EDIT-:' + str(valueIndex) + ':BLUE', enable_events=True))
                colorAndSpecularBlock[3].append(sg.InputText(str(specValue['specular'][2]), size=(15, 1), key='-SINGLE-SPECULAR-EDIT-:' + str(valueIndex) + ':BLUE', enable_events=True))
            if gvars.editedTextureName != None and valueIndex < gvars.maxSpecularValuesAmount: # When we need to update an existing element value
                gvars.second_window['-SINGLE-COLOR-EDIT-:' + str(valueIndex) + ':RED'].update(visible=True, value=str(specValue['color'][0]))
                gvars.second_window['-SINGLE-SPECULAR-EDIT-:' + str(valueIndex) + ':RED'].update(visible=True, value=str(specValue['specular'][0]))
                gvars.second_window['-SINGLE-COLOR-EDIT-:' + str(valueIndex) + ':GREEN'].update(visible=True, value=str(specValue['color'][1]))
                gvars.second_window['-SINGLE-SPECULAR-EDIT-:' + str(valueIndex) + ':GREEN'].update(visible=True, value=str(specValue['specular'][1]))
                gvars.second_window['-SINGLE-COLOR-EDIT-:' + str(valueIndex) + ':BLUE'].update(visible=True, value=str(specValue['color'][2]))
                gvars.second_window['-SINGLE-SPECULAR-EDIT-:' + str(valueIndex) + ':BLUE'].update(visible=True, value=str(specValue['specular'][2]))
                gvars.second_window['-SINGLE-SPECULAR-COLOR-:' + str(valueIndex)].update(visible=True, background_color=hexColor)
                gvars.second_window['-SINGLE-SPECULAR-SPECULAR-:' + str(valueIndex)].update(visible=True, background_color=hexSpecular)
        if gvars.editedTextureName == None or valueIndex >= gvars.maxSpecularValuesAmount: # If there are new values to display (more than previously met), appends them to the layout
            gvars.second_window.extend_layout(gvars.second_window['-SPECULAR-MAP-VALUES-'], colorAndSpecularBlock)
    if (specValuesAmount < gvars.specularValuesAmount): # If there are less values than previously met, hides the elements that are not needed anymore
        for i in range(specValuesAmount, gvars.specularValuesAmount):
            gvars.second_window['-SINGLE-SPECULAR-COLOR-:' + str(i)].update(visible=False)
            gvars.second_window['-SINGLE-SPECULAR-SPECULAR-:' + str(i)].update(visible=False)
            gvars.second_window['-SINGLE-COLOR-RED-TEXT-:' + str(i)].update(visible=False)
            gvars.second_window['-SINGLE-COLOR-EDIT-:' + str(i) + ':RED'].update(visible=False)
            gvars.second_window['-SINGLE-SPECULAR-EDIT-:' + str(i) + ":RED"].update(visible=False)
            gvars.second_window['-SINGLE-COLOR-GREEN-TEXT-:' + str(i)].update(visible=False)
            gvars.second_window['-SINGLE-COLOR-EDIT-:' + str(i) + ':GREEN'].update(visible=False)
            gvars.second_window['-SINGLE-SPECULAR-EDIT-:' + str(i) + ":GREEN"].update(visible=False)
            gvars.second_window['-SINGLE-COLOR-BLUE-TEXT-:' + str(i)].update(visible=False)
            gvars.second_window['-SINGLE-COLOR-EDIT-:' + str(i) + ':BLUE'].update(visible=False)
            gvars.second_window['-SINGLE-SPECULAR-EDIT-:' + str(i) + ":BLUE"].update(visible=False)
    if (specValuesAmount > gvars.maxSpecularValuesAmount):
        gvars.maxSpecularValuesAmount = specValuesAmount
    gvars.specularValuesAmount = specValuesAmount