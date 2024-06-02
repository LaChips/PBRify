from enum import Enum
from src.createSpecularMaps import createSpecularMap
import src.vars as gvars
from src.textureEditor import displayMaps, displaySpecularValues

SPECULAR_RGB_MAP = Enum('SPECULAR_RGB_MAP', ['RED', 'GREEN', 'BLUE'])

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
        gvars.second_window['-SINGLE-FAST-'].update(value=texture.fastSpecular if texture.fastSpecular != None else gvars.fastSpecular)
        gvars.second_window['-INVERT-NORMAL-RED-'].update(value=texture.reversedNormalsRed if texture.reversedNormalsRed != None else False)
        gvars.second_window['-INVERT-NORMAL-GREEN-'].update(value=texture.reversedNormalsGreen if texture.reversedNormalsGreen != None else False)
        gvars.second_window['-INVERT-HEIGHT-'].update(value=texture.reversedHeight if texture.reversedHeight != None else False)
        gvars.second_window['-SINGLE-NORMAL-'].update(value=texture.normalIntensity if texture.normalIntensity != None else 1)
        gvars.second_window['-SINGLE-HEIGHT-'].update(value=texture.heightIntensity if texture.heightIntensity != None else 0.12)
        gvars.second_window['-SINGLE-HEIGHT-BRIGHTNESS-'].update(value=texture.heightBrightness if texture.heightBrightness != None else 1)
        if texture == None or textureName == gvars.editedTextureName:
            print("texture not found")
            return
        if (texture.name in gvars.textures_data):
            displayMaps(texture,  texture.name)
            displaySpecularValues(texture, texture.name)
            gvars.editedTexture = texture
            gvars.editedTextureName = texture.name
            texturesValues = gvars.textures_data[texture.name]
            texture.customValues = texturesValues
            gvars.second_window['-SPECULAR-MAP-VALUES-'].contents_changed()
            gvars.second_window['-SPECULAR-MAP-VALUES-'].contents_changed()
    elif event2 == '-INVERT-NORMAL-RED-':
        gvars.editedTexture.reversedNormalsRed = values2['-INVERT-NORMAL-RED-']
    elif event2 == '-INVERT-NORMAL-GREEN-':
        gvars.editedTexture.reversedNormalsGreen = values2['-INVERT-NORMAL-GREEN-']
    elif event2 == '-INVERT-HEIGHT-':
        gvars.editedTexture.reversedHeight = values2['-INVERT-HEIGHT-']
    elif event2 == '-SINGLE-NORMAL-':
        gvars.editedTexture.normalIntensity = values2['-SINGLE-NORMAL-']
    elif event2 == '-SINGLE-HEIGHT-':
        gvars.editedTexture.heightIntensity = values2['-SINGLE-HEIGHT-']
    elif event2 == '-SINGLE-HEIGHT-BRIGHTNESS-':
        gvars.editedTexture.heightBrightness = values2['-SINGLE-HEIGHT-BRIGHTNESS-']
    elif event2.split(':')[0] == '-SINGLE-SPECULAR-EDIT-':
        value = int(values2[event2]) # R/G/B value
        customValuesIndex = int(event2.split(':')[1]) # Index of the value in the customValues array
        colorIndex = SPECULAR_RGB_MAP[event2.split(':')[2]].value - 1 # Index of the color in the RGB array (RED = 0, GREEN = 1, BLUE = 2)
        gvars.editedTexture.customValues[customValuesIndex]['specular'][colorIndex] = value
        gvars.second_window['-SINGLE-SPECULAR-SPECULAR-:' + event2.split(':')[1]].update(background_color='#' + ('{:02X}' * 3).format(
            value if colorIndex == 0 else gvars.editedTexture.customValues[customValuesIndex]['specular'][0], # RED
            value if colorIndex == 1 else gvars.editedTexture.customValues[customValuesIndex]['specular'][1], # GREEN
            value if colorIndex == 2 else gvars.editedTexture.customValues[customValuesIndex]['specular'][2] # BLUE
        ))
    elif event2.split(':')[0] == '-SINGLE-COLOR-EDIT-':
        value = int(values2[event2]) # R/G/B value
        customValuesIndex = int(event2.split(':')[1]) # Index of the value in the customValues array
        colorIndex = SPECULAR_RGB_MAP[event2.split(':')[2]].value - 1 # Index of the color in the RGB array (RED = 0, GREEN = 1, BLUE = 2)
        gvars.editedTexture.customValues[customValuesIndex]['color'][colorIndex] = value
        gvars.second_window['-SINGLE-SPECULAR-COLOR-:' + event2.split(':')[1]].update(background_color='#' + ('{:02X}' * 3).format(
            value if colorIndex == 0 else gvars.editedTexture.customValues[customValuesIndex]['color'][0], # RED
            value if colorIndex == 1 else gvars.editedTexture.customValues[customValuesIndex]['color'][1], # GREEN
            value if colorIndex == 2 else gvars.editedTexture.customValues[customValuesIndex]['color'][2] # BLUE
        ))
    elif event2 == '-SINGLE-FAST-':
        gvars.editedTexture.fastSpecular = values2['-SINGLE-FAST-']
    elif event2 == '-CONVERT-TEXTURE-':
        createSpecularMap(gvars.editedTexture)
