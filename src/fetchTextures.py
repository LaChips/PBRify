import os
from os import listdir
from os.path import isfile, join
from src.Texture import texture

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
    "glowstone.png",
    "kelp.png",
    "kelp_plant.png",
    "lantern.png",
    "lava_flow.png",
    "lava_still.png",
    "magma.png",
    "nether_portal.png",
    "prismarine.png",
    "pumpkin_face_on.png",
    "redstone_lamp_on.png",
    "repeating_command_block_back.png",
    "repeating_command_block_conditional.png",
    "repeating_command_block_front.png",
    "repeating_command_block_side.png",
    "respawn_anchor_top.png",
    "sea_lantern.png",
    "seagrass.png",
    "smoker_front_on.png",
    "soul_campfire_fire.png",
    "soul_campfire_log_lit.png",
    "soul_fire_0.png",
    "soul_fire_1.png",
    "soul_lantern.png",
    "stonecutter_saw.png",
    "tall_seagrass_bottom.png",
    "tall_seagrass_top.png",
    "warped_stem.png",
    "water_flow.png",
    "water_still.png",
    ""
]

def listTextures(window, textures, path):
    files = [f for f in listdir(path)]
    i = 1;
    for file in files:
        window['progress'].update(i, len(files))
        if (os.path.isdir(join(path, file)) == True):
            listTextures(window, textures, join(path, file))
        elif ("png" in file and ("mcmeta" not in file) and (file not in excluded_names) and os.path.isfile(join(path, file))):
            textures.append(texture(path + "/", file.split('.')[0], '.' + file.split('.')[1]))
        i = i+1

def getTextures(window, base_path):
    textures = []
    window['state'].update(value="Fetching textures")
    texture_path = os.path.join(base_path, os.path.join('pack_unziped', 'assets', 'minecraft', 'textures'))
    print("texture_path :", texture_path)
    listTextures(window, textures, os.path.join(texture_path, 'block'))
    #listTextures(window, textures, os.path.join(texture_path, 'block_alt'))
    listTextures(window, textures, os.path.join(texture_path, 'item'))
    #listTextures(window, textures, os.path.join(texture_path, 'item_alt'))
    return textures