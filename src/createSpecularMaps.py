import cv2
from pylab import array, arange, uint8
import src.vars as gvars
from PIL import Image, ImageDraw
import numpy as np
import os.path
import math
import json
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from multiprocessing import Process

import numpy

def patch_asscalar(a):
    return a.item()

setattr(numpy, "asscalar", patch_asscalar)

# This method is way faster but also more error prone

def getFastDistance(color1, color2):
    cR=color1[0]-color2[0]
    cG=color1[1]-color2[1]
    cB=color1[2]-color2[2]
    uR=color1[0]+color2[0]
    distance=cR*cR*(2+uR/256) + cG*cG*4 + cB*cB*(2+(255-uR)/256)
    return distance

def getDistance(color1, color2):
    d = 10000
    try:
        color1_rgb = sRGBColor(color1[0], color1[1], color1[2])
        color2_rgb = sRGBColor(color2[0], color2[1], color2[2])
        # Convert from RGB to Lab Color Space
        color1_lab = convert_color(color1_rgb, LabColor)
        # Convert from RGB to Lab Color Space
        color2_lab = convert_color(color2_rgb, LabColor)
        d = delta_e_cie2000(color1_lab, color2_lab)
    except Exception as e:
        print("error getting color distance: ", e)
    return d

def closest(colors,c2):
    smallest_idx = -1
    smallest_dist = 10000
    d = 10000
    #print("c2 :", c2)
    for i in range(0, len(colors)):
        #print("colors[i] :", colors[i])
        if (gvars.fastSpecular):
            d = getFastDistance(colors[i], c2)
        else:
            d = getDistance(colors[i], c2)
        #print("d :" + d)
        if (d < smallest_dist):
            smallest_idx = i
            smallest_dist = d
    return smallest_idx

def getSpecularForColor(texture_name, color, textures_data):
    colors = []
    if texture_name in textures_data:
        for color_data in textures_data[texture_name]:
            colors.append(color_data['color'])
        try:
            index = closest(colors, color)
        except:
            return (0, 0, 0)
        if index == -1:
            return (0, 0, 0)
        return textures_data[texture_name][index]['specular']
    else:
        return (0, 0, 0)

def processTexture(texture, i, textures_data):
    print("texture.name :", texture.name)
    diffuse = None
    try:
        diffuse = Image.open(r"" + os.path.join(texture.path, texture.name + texture.ext), 'r', ['png']).convert('RGB')
    except:
        print("can't load texture " + texture.name)
        return
    size = diffuse.size[0]
    texture_data = diffuse.load()
    img = Image.new('RGB', (size, size))
    spec_image = img.load()
    for idx in range(0, size * size):
        try:
            spec = getSpecularForColor(texture.name, texture_data[idx % size, int(idx / size)], textures_data)
            spec_image[idx % size, int(idx / size)] = (spec[0], spec[1], spec[2])
        except Exception as e:
            print('failed to process ' + texture.name + ":" + str(e))
            return
    img.save(texture.path + texture.name + '_s' + texture.ext)

def createSpecularMaps(textures):
    print("fastSpecular :", gvars.fastSpecular)
    gvars.window['state'].update(value="Generating specular maps")
    for i in range(0, len(textures)):
        gvars.window['progress'].update(i + 1, len(textures))
        gvars.window['state'].update(value="Generating specular map for " + textures[i].name)
        processTexture(textures[i], i, gvars.textures_data)
        