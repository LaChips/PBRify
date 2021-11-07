import cv2
from pylab import array, arange, uint8

def createHeightMaps(window, textures):
    window['state'].update(value="Generating height maps")
    i = 1;
    for textureData in textures:
        window['progress'].update(i, len(textures))
        try:
            normal = cv2.imread(textureData.path + textureData.name + "_n" + textureData.ext)
            gray = cv2.imread(textureData.path + textureData.name + textureData.ext, 0)
            gray[gray < 255-30] += 30
            maxIntensity = 255.0 # depends on dtype of image data
            x = arange(maxIntensity) 
            phi = 1
            theta = 1
            toHeightMap = (maxIntensity/phi)*(gray/(maxIntensity/theta))**0.1
            heightMap = array(toHeightMap,dtype=uint8)
            rgba = cv2.cvtColor(normal, cv2.COLOR_RGB2RGBA)
            rgba[:, :, 3] = heightMap
            cv2.imwrite(textureData.path + textureData.name + "_n" + textureData.ext, rgba)
        except:
            print("no normal map for " + textureData.name)
        i = i+1