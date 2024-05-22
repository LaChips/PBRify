import os
import shutil
import json
from src.copyPackAndUnzip import copyPackAndUnzip

import src.vars as gvars

def start():
    print("gvars :", gvars)
    if (os.path.isfile(os.path.join(gvars.base_path, 'pack.zip'))):
        os.remove(os.path.join(gvars.base_path, 'pack.zip'))
    if (os.path.isdir(os.path.join(gvars.base_path, 'pack_unziped'))):
        shutil.rmtree(os.path.join(gvars.base_path, 'pack_unziped'), ignore_errors=True)
    copyPackAndUnzip()
    gvars.window['state'].update(visible=True)
    gvars.window['progress'].update(visible = True)
    with open(os.path.join(gvars.base_path, 'lib/textures_data.json'), 'r') as json_file:
        gvars.textures_data = json.loads(json_file.read())
    #repackTextures(gvars.pack.split('/')[len(gvars.pack.split('/')) - 1].split('.zip')[0] + "_PBR_" +  "fast" if gvars.fastSpecular else "slow")