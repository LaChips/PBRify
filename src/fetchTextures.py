import os
from PIL import Image
from os import listdir
from os.path import isfile, isdir, join
from src.texture import Texture
from src.vars import UNZIP_DIR

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.pbrify import Converter  # This import is only for type checking

excluded_names = [
    "blast_furnace_front_on.png",
    "campfire_fire.png",
    "campfire_log_lit.png",
    "chain_command_block_back.png",
    "chain_command_block_conditional.png",
    "chain_command_block_front.png",
    "chain_command_block_side.png",
    "command_block_back.png",
    "command_block_conditional.png",
    "command_block_front.png",
    "command_block_side.png",
    "crimson_stem.png",
    "fire_0.png",
    "fire_1.png",
    "kelp.png",
    "kelp_plant.png",
    "lava_flow.png",
    "lava_still.png",
    "nether_portal.png",
    "pumpkin_face_on.png",
    "redstone_lamp_on.png",
    "repeating_command_block_back.png",
    "repeating_command_block_conditional.png",
    "repeating_command_block_front.png",
    "repeating_command_block_side.png",
    "respawn_anchor_top.png",
    "seagrass.png",
    "smoker_front_on.png",
    "soul_campfire_fire.png",
    "soul_campfire_log_lit.png",
    "soul_fire_0.png",
    "soul_fire_1.png",
    "stonecutter_saw.png",
    "tall_seagrass_bottom.png",
    "tall_seagrass_top.png",
    "warped_stem.png",
    "water_flow.png",
    "water_still.png",
]

class TextureFetcher:
    def __init__(self, converter : 'Converter'):
        self.app = converter.app
        self.config = converter.config
        self.base_path = self.config.base_path

    def listTextures(self, normals, speculars, path):
        if isdir(path):
            files = [f for f in listdir(path)]
            i = 1
            for file in files:
                self.app.updateProgressBar(i, len(files))
                if isdir(join(path, file)):
                    self.listTextures(normals, speculars, join(path, file))
                elif "png" in file and "sapling" not in file and "mcmeta" not in file and file not in excluded_names and isfile(join(path, file)):
                    texture_obj = Texture(path + "/", file.split('.')[0], '.' + file.split('.')[1])
                    texture_obj.create_thumbnail()  # Generate thumbnail here
                    if file.split('.')[0] in self.config.normals:
                        normals.append(texture_obj)
                    if file.split('.')[0] in self.config.speculars:
                        speculars.append(texture_obj)
                i += 1


    def getTextures(self):
        normals = []
        speculars = []
        self.app.updateStateText("Fetching textures")
        texture_path = os.path.join(self.base_path, os.path.join(UNZIP_DIR, 'assets', 'minecraft', 'textures'))
        self.listTextures(normals, speculars, os.path.join(texture_path, "blocks"))
        self.listTextures(normals, speculars, os.path.join(texture_path, "block"))
        self.listTextures(normals, speculars, os.path.join(texture_path, "items"))
        self.listTextures(normals, speculars, os.path.join(texture_path, "item"))
        # listTextures(normals, speculars, os.path.join(texture_path, "entities"))
        # listTextures(normals, speculars, os.path.join(texture_path, "entity"))
        return {'normals': normals, 'speculars': speculars}