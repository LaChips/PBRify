import os
from os import listdir
from os.path import isfile, isdir, join
from src.Texture import texture
import src.vars as gvars

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

def listTextures(normals, speculars, diffuses, path):
    if isdir(path) == True:
        files = [f for f in listdir(path)]
        i = 1
        for file in files:
            gvars.window['progress'].update(i, len(files))
            if (os.path.isdir(join(path, file)) == True):
                listTextures(normals, speculars, diffuses, join(path, file))
            elif ("png" in file and "sapling" not in file and ("mcmeta" not in file) and (file not in excluded_names)and os.path.isfile(join(path, file))):
                if file.split('.')[0] in gvars.normals:
                    normals.append(texture(path + "/", file.split('.')[0], '.' + file.split('.')[1]))
                if file.split('.')[0] in gvars.speculars:
                    speculars.append(texture(path + "/", file.split('.')[0], '.' + file.split('.')[1]))
                diffuses.append(texture(path + "/", file.split('.')[0], '.' + file.split('.')[1]))
            i = i+1

def getTextures():
    normals = []
    speculars = []
    diffuses = []
    gvars.window['state'].update(value="Fetching textures")
    texture_path = os.path.join(gvars.base_path, os.path.join('pack_unziped', 'assets', 'minecraft', 'textures'))
    listTextures(normals, speculars, diffuses, os.path.join(texture_path, "blocks"))
    listTextures(normals, speculars, diffuses, os.path.join(texture_path, "block"))
    listTextures(normals, speculars, diffuses, os.path.join(texture_path, "items"))
    listTextures(normals, speculars, diffuses, os.path.join(texture_path, "item"))
    # listTextures(normals, speculars, os.path.join(texture_path, "entities"))
    # listTextures(normals, speculars, os.path.join(texture_path, "entity"))
    return {'normals': normals, 'speculars': speculars, 'diffuses': diffuses}