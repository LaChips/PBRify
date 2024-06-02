from createHeightMaps import createHeightMap, createHeightMaps
from createNormalsMaps import createNormal, createNormals
import src.vars as gvars
from textureEditor import displayMaps

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