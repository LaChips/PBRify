import src.vars as gvars

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