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

def createHeightMaps(textures):
    gvars.window['state'].update(value="Generating height maps")
    for i in range(0, len(textures)):
        if textures[i].name not in gvars.normals:
            continue
        gvars.window['progress'].update(i + 1, len(textures))
        try:
            normal = cv2.imread(textures[i].path + textures[i].name + "_n" + textures[i].ext)
        except:
            print("no normal map for " + textures[i].name)
            i = i+1
            continue
        diffuse = cv2.imread(textures[i].path + textures[i].name + textures[i].ext, 0)
        diffuse[diffuse < 255-50] += 50
        maxIntensity = 255.0 # depends on dtype of image data
        x = arange(maxIntensity) 
        phi = 1
        theta = 1
        toHeightMap = (maxIntensity/phi)*(diffuse/(maxIntensity/theta))**gvars.heightIntensity
        heightMap = array(toHeightMap,dtype=uint8)
        # try:
        #     print("smoothing edges of " + textures[i].name)
        #     heightMap = smoothEdges(heightMap)
        # except:
        #    print("Error while smoothing " + textures[i].name + " edges")
        try:

            rgba = cv2.cvtColor(normal, cv2.COLOR_RGB2RGBA)
            rgba[:, :, 3] = heightMap
            cv2.imwrite(textures[i].path + textures[i].name + "_n" + textures[i].ext, rgba)
            cv2.destroyAllWindows()
        except:
            print("Error while inserting heightMap in normalMap alpha channel")
            i = i+1
            continue
        i = i+1