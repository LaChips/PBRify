import os
import shutil
import json
import zipfile
import threading
from src.fetchTextures import TextureFetcher
from src.createNormalsMaps import createNormals
from src.createHeightMaps import createHeightMaps
from src.createSpecularMaps import createSpecularMaps
from src.vars import Config, AppState, UNZIP_DIR

class Converter:

    def __init__(self, config : Config, app : AppState):
        self.config = config
        self.app = app
        self.normals = []
        self.speculars = []
        self.texture_data = None

    def start(self):
        config = self.config
        print("configuration :", config)
        if (os.path.isfile(os.path.join(config.base_path, 'pack.zip'))):
            os.remove(os.path.join(config.base_path, 'pack.zip'))
        if (os.path.isdir(os.path.join(config.base_path, UNZIP_DIR))):
            shutil.rmtree(os.path.join(config.base_path, UNZIP_DIR), ignore_errors=True)

        self.copyPackAndUnzip()

        self.app.window['state'].update(visible=True)
        self.app.window['progress'].update(visible = True)

        with open(os.path.join(config.base_path, 'lib/textures_data.json'), 'r') as json_file:
            self.textures_data = json.loads(json_file.read())

        textureFetcher = TextureFetcher(self)

        textures = textureFetcher.getTextures()

        self.normals = config.normals
        self.speculars = config.speculars

        createSpecularMaps(textures['speculars'], self)
        createNormals(textures['normals'], self)
        createHeightMaps(textures['normals'], self)

        self.repackTextures(config.pack.split('/')[len(config.pack.split('/')) - 1].split('.zip')[0] + "_PBR")

    def copyPackAndUnzip(self):
        if self.config.pack.index('.zip') == -1:
            return
        cwd = os.path.join(self.config.base_path, "pack.zip")
        shutil.copyfile(self.config.pack, cwd)
        with zipfile.ZipFile(cwd, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(self.config.base_path, UNZIP_DIR))

    def repackTextures(self, output_filename):
        self.app.window['state'].update(value="repacking "+output_filename+" in "+ self.config.directory)
        if (os.path.isfile(self.config.directory + "/" + output_filename)):
            os.remove(self.config.directory + "/" + output_filename, 'zip')
        x = threading.Thread(target=self.thread_function, args=(output_filename,))
        x.start()

    def thread_function(self, path):
        shutil.make_archive(self.config.directory + "/" + path, 'zip', os.path.join(self.config.base_path, UNZIP_DIR))
        self.app.done = True