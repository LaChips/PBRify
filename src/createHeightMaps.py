import os
import cv2
from pylab import array, arange, uint8
import src.vars as gvars
import math

# None of the 3 attemps below are satisfying
#
# def smoothEdges(HM):
#     for x in range(0, len(HM) - 1):
#         try:
#             HM[0][x] = 255
#             HM[len(HM) - 1][x] = 255
#         except:
#             continue
#     for y in range(0, len(HM) - 1):
#         try:
#             HM[y][0] = 255
#             HM[y][len(HM) - 1] = 255
#         except:
#             continue
#     return HM

# def smoothEdges(HM):
#     imgsize = len(HM);
#     for y in range(0, imgsize):
#         for x in range(0, imgsize):
#             distanceToCenter = math.sqrt((x - imgsize/2) ** 2 + (y - imgsize/2) ** 2)
#             distanceToCenter = float(distanceToCenter) / (math.sqrt(2) * imgsize/2)
#             level =  HM[y][x] + distanceToCenter * (255 - HM[y][x])
#              # Or just
#              # r = innerColor[0]
#              # g = innerColor[1]
#              # b = innerColor[2]
#              # if not blending with white as you get farther away from the center.
#             HM[y][x] = distanceToCenter * 255

# # def smoothEdges(HM):
# #     size = math.floor(len(HM))
# #     limit = math.ceil(size / 5)
# #     #print("size :", size)
# #     for y in range(0, math.floor(size / 2)):
# #         iLimit = 0
# #         for x in range(0, size):
# #             if y == 0 or (x >= 0 and x <= (size / 2) / y):
# #                 try:
# #                     #print(HM[y][x])
# #                     if y == 0:
# #                         HM[x][y] = 255
# #                     elif HM[x][y] < 255:
# #                         HM[x][y] += 255 - HM[x][y]# - y  - x
# #                     #elif HM[size - y][size - x] < 250:
# #                     #    HM[size - y][size - x] += 250 - HM[size - y][size - x]# - (size - y) - x
# #                 except:
# #                     continue
# #     return HM

def toHeight(texture):
    # if texture.name not in gvars.normals:
    #     return
    try:
        normal = cv2.imread(texture.path + texture.name + "_n" + texture.ext)
    except:
        print("no normal map for " + texture.name)
        return
    diffuse = cv2.imread(texture.path + texture.name + texture.ext, 0)
    resizedDiffuse = diffuse[:diffuse.shape[1],:diffuse.shape[1]]
    brightness = texture.heightBrightness if texture.heightBrightness != None else 1
    resizedDiffuse[resizedDiffuse < 255-(int(50 * brightness))] += int(50 * brightness)
    maxIntensity = 255.0 # depends on dtype of image data
    x = arange(maxIntensity) 
    phi = 1
    theta = 1
    contrast = (texture.heightIntensity if texture.heightIntensity != None else gvars.heightIntensity)
    toHeightMap = (maxIntensity/phi)*(resizedDiffuse/(maxIntensity/theta))**contrast
    heightMap = array(toHeightMap,dtype=uint8)
    if (texture.reversedHeight == True):
        lowest = heightMap.min()
        highest = heightMap.max()
        heightMap = highest - heightMap + lowest
    # try:
    #     print("smoothing edges of " + texture.name)
    #     heightMap = smoothEdges(heightMap)
    # except:
    #    print("Error while smoothing " + texture.name + " edges")
    try:
        rgba = cv2.cvtColor(normal, cv2.COLOR_RGB2RGBA)
        rgba[:, :, 3] = heightMap
        cv2.imwrite(texture.path + texture.name + "_n" + texture.ext, rgba)
        cv2.imwrite(texture.path + texture.name + "_h" + texture.ext, heightMap)
        cv2.destroyAllWindows()
    except:
        print("Error while inserting heightMap in normalMap alpha channel")
    #gvars.window.write_event_value(('-THREAD-', '-HEIGHT-THREAD-ENDED-'), '-HEIGHT-THREAD-ENDED-')

def threaded_process(textures):
    for i in range(0, len(textures)):
        gvars.window.write_event_value(('-HEIGHT-GENERATION-', textures[i].name + ':' + str(i)), textures[i].name + ':' + str(i))
        #gvars.window['progress'].update(i + 1, len(textures))
        textureNameWithRelativePath = textures[i].path.split(os.path.join(gvars.base_path, os.path.join('pack_unziped', 'assets', 'minecraft', 'textures')))[1] + textures[i].name
        # if textures[i].name not in gvars.normals or textureNameWithRelativePath in gvars.blocks_to_ignore:
        #     continue
        if textureNameWithRelativePath in gvars.blocks_to_ignore:
            continue
        try:
            toHeight(textures[i])
        except SyntaxError:
            print("Broken png file : " + textures[i].path + textures[i].name + textures[i].ext)
        i = i+1
    #gvars.window.write_event_value(('-THREAD-', '-HEIGHT-THREAD-ENDED-'), '-HEIGHT-THREAD-ENDED-')

def createHeightMaps(textures):
    gvars.window.start_thread(lambda: threaded_process(textures), ('-THREAD-', '-HEIGHT-THREAD-ENDED-'))

def createHeightMap(texture):
    gvars.window.start_thread(lambda: threaded_process([texture]), ('-THREAD-', '-SINGLE-HEIGHT-THREAD-ENDED-'))
