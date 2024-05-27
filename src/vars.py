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
editedTexture = {}
editedTextureName = None
maxSpecularValuesAmount = 0
specularValuesAmount = 0
plant_blocks = [
    "\\block/acacia_sapling",
    "\\block/birch_sapling",
    "\\block/dark_oak_sapling",
    "\\block/jungle_sapling",
    "\\block/oak_sapling",
    "\\block/spruce_sapling",
    "\\block/allium",
    "\\block/azure_bluet",
    "\\block/blue_orchid",
    "\\block/cornflower",
    "\\block/dandelion",
    "\\block/lilac_top",
    "\\block/lilac_bottom",
    "\\block/lily_of_the_valley",
    "\\block/orange_tulip",
    "\\block/oxeye_daisy",
    "\\block/peony_top",
    "\\block/peony_bottom",
    "\\block/pink_tulip",
    "\\block/poppy",
    "\\block/red_tulip",
    "\\block/rose_bush_top",
    "\\block/rose_bush_bottom",
    "\\block/sunflower_back",
    "\\block/sunflower_front",
    "\\block/sunflower_bottom",
    "\\block/sunflower_top",
    "\\block/white_tulip",
    "\\block/wither_rose",
    "\\block/brown_mushroom",
    "\\block/red_mushroom",
    "\\block/hanging_roots",
    "\\block/spore_blossom",
    "\\block/small_dripleaf_top_extra",
    "\\block/small_dripleaf_top",
    "\\block/small_dripleaf_stem_top",
    "\\block/small_dripleaf_stem_bottom",
    "\\block/big_dripleaf_stem",
    "\\block/big_dripleaf_tip",
    "\\block/big_dripleaf_top",
    "\\block/big_dripleaf_tip_extra",
    "\\block/big_dripleaf_top_extra",
    "\\block/dead_bush",
    "\\block/fern",
    "\\block/large_fern_bottom",
    "\\block/large_fern_top",
    "\\block/short_grass",
    "\\block/tall_grass_bottom",
    "\\block/tall_grass_top",
    "\\block/tall_seagrass_bottom",
    "\\block/tall_seagrass_top",
    #"vines"
    "\\block/beetroots_stage0",
    "\\block/beetroots_stage1",
    "\\block/beetroots_stage2",
    "\\block/beetroots_stage3",
    "\\block/carrots_stage0",
    "\\block/carrots_stage1",
    "\\block/carrots_stage2",
    "\\block/carrots_stage3",
    "\\block/potatoes_stage0",
    "\\block/potatoes_stage1",
    "\\block/potatoes_stage2",
    "\\block/potatoes_stage3",
    "\\block/wheat",
    "\\block/sweet_berries",
    "\\block/nether_wart_stage0",
    "\\block/nether_wart_stage1",
    "\\block/nether_wart_stage2",
    "\\block/cocoa_stage0",
    "\\block/cocoa_stage1",
    "\\block/cocoa_stage2",
]