import os
import shutil
from src.copyPackAndUnzip import copyPackAndUnzip
from src.fetchTextures import getTextures, listTextures
from src.createNormalsMaps import createNormals
from src.createHeightMaps import createHeightMaps
from src.repackTextures import repackTextures

def start(window, pack, directory, base_path):
    if (os.path.isfile(os.path.join(base_path, 'pack.zip'))):
        os.remove(os.path.join(base_path, 'pack.zip'))
    if (os.path.isdir(os.path.join(base_path, 'pack_unziped'))):
        shutil.rmtree(os.path.join(base_path, 'pack_unziped'), ignore_errors=True)
    copyPackAndUnzip(pack, base_path)
    window['state'].update(visible=True)
    window['progress'].update(visible = True)
    textures = getTextures(window, base_path)
    createNormals(window, textures)
    createHeightMaps(window, textures)
    repackTextures(window, pack.split('/')[len(pack.split('/')) - 1].split('.zip')[0] + "_PBR", directory, base_path)
    os.remove(os.path.join(base_path, 'pack.zip'))
    shutil.rmtree(os.path.join(base_path, 'pack_unziped'), ignore_errors=True)
    window['state'].update(value="Done!")
