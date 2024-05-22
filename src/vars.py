window = None
second_window = None
directory = None
pack = None
base_path = None
normalIntensity = 1
heightIntensity = 0.1
done = False
textures_data = None
normals = []
speculars = []
fastSpecular = False
blocks_to_ignore = []
blocks_to_ignore_tmp = []
plant_blocks = [
    "acacia_sapling",
    "birch_sapling",
    "dark_oak_sapling",
    "jungle_sapling",
    "oak_sapling",
    "spruce_sapling",
    "allium",
    "azure_bluet",
    "blue_orchid",
    "cornflower",
    "dandelion",
    "lilac_top",
    "lilac_bottom",
    "lily_of_the_valley",
    "orange_tulip",
    "oxeye_daisy",
    "peony_top",
    "peony_bottom",
    "pink_tulip",
    "poppy",
    "red_tulip",
    "rose_bush_top",
    "rose_bush_bottom",
    "sunflower_back",
    "sunflower_front",
    "sunflower_bottom",
    "sunflower_top",
    "white_tulip",
    "wither_rose",
    "brown_mushroom",
    "red_mushroom",
    "hanging_roots",
    "spore_blossom",
    "small_dripleaf_top_extra",
    "small_dripleaf_top",
    "small_dripleaf_stem_top",
    "small_dripleaf_stem_bottom",
    "big_dripleaf_stem",
    "big_dripleaf_tip",
    "big_dripleaf_top",
    "big_dripleaf_tip_extra",
    "big_dripleaf_top_extra",
    "dead_bush",
    "fern",
    "large_fern_bottom",
    "large_fern_top",
    "short_grass",
    "tall_grass_bottom",
    "tall_grass_top",
    "tall_seagrass_bottom",
    "tall_seagrass_top",
    #"vines"
    "beetroots_stage0",
    "beetroots_stage1",
    "beetroots_stage2",
    "beetroots_stage3",
    "carrots_stage0",
    "carrots_stage1",
    "carrots_stage2",
    "carrots_stage3",
    "potatoes_stage0",
    "potatoes_stage1",
    "potatoes_stage2",
    "potatoes_stage3",
    "wheat",
    "sweet_berries",
    "nether_wart_stage0",
    "nether_wart_stage1",
    "nether_wart_stage2",
    "cocoa_stage0",
    "cocoa_stage1",
    "cocoa_stage2",
]