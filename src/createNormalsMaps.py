import os
import imageio
import scipy.ndimage
import numpy as np
import src.vars as gvars

def smooth_gaussian(im, sigma):

    if sigma == 0:
        return im

    im_smooth = im.astype(float)
    kernel_x = np.arange(-3*sigma,3*sigma+1).astype(float)
    kernel_x = np.exp((-(kernel_x**2))/(2*(sigma**2)))

    im_smooth = scipy.ndimage.convolve(im_smooth, kernel_x[np.newaxis])

    im_smooth = scipy.ndimage.convolve(im_smooth, kernel_x[np.newaxis].T)

    return im_smooth


def gradient(im_smooth):

    gradient_x = im_smooth.astype(float)
    gradient_y = im_smooth.astype(float)

    kernel = np.arange(-1,2).astype(float)
    kernel = - kernel / 2

    gradient_x = scipy.ndimage.convolve(gradient_x, kernel[np.newaxis])
    gradient_y = scipy.ndimage.convolve(gradient_y, kernel[np.newaxis].T)

    return gradient_x,gradient_y


def sobel(im_smooth):
    gradient_x = im_smooth.astype(float)
    gradient_y = im_smooth.astype(float)

    kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

    gradient_x = scipy.ndimage.convolve(gradient_x, kernel)
    gradient_y = scipy.ndimage.convolve(gradient_y, kernel.T)

    return gradient_x,gradient_y


def compute_normal_map(gradient_x, gradient_y, normalIntensity):
    width = gradient_x.shape[1]
    height = gradient_x.shape[0]
    max_x = np.max(gradient_x)
    max_y = np.max(gradient_y)

    max_value = max_x

    if max_y > max_x:
        max_value = max_y

    normal_map = np.zeros((height, width, 3), dtype=np.float32)

    intensity = 1 / normalIntensity if normalIntensity != None else gvars.normalIntensity

    strength = max_value / (max_value * intensity)

    normal_map[..., 0] = gradient_x / max_value
    normal_map[..., 1] = gradient_y / max_value
    normal_map[..., 2] = 1 / strength

    norm = np.sqrt(np.power(normal_map[..., 0], 2) + np.power(normal_map[..., 1], 2) + np.power(normal_map[..., 2], 2))

    normal_map[..., 0] /= norm
    normal_map[..., 1] /= norm
    normal_map[..., 2] /= norm

    normal_map *= 0.5
    normal_map += 0.5

    data = 255 * normal_map # Now scale by 255
    normals = data.astype(np.uint8)
    return normals

def toNormal(texture):
    sigma = 0
    input_file = texture.path + texture.name + texture.ext
    output_file = texture.path + texture.name + '_n' + texture.ext

    try:
        im = imageio.imread(input_file, pilmode="RGBA")
        resizedIm = im[:im.shape[1],:im.shape[1]]
    except:
        print("can't read " + texture.name)
        return -1

    if resizedIm.ndim == 3:
        im_grey = np.zeros((resizedIm.shape[0],resizedIm.shape[1])).astype(float)
        im_grey = (resizedIm[...,0] * 0.3 + resizedIm[...,1] * 0.6 + resizedIm[...,2] * 0.1)
        resizedIm = im_grey

    im_smooth = smooth_gaussian(resizedIm, sigma)

    sobel_x, sobel_y = sobel(im_smooth)

    normal_map = compute_normal_map(sobel_x, sobel_y, texture.normalIntensity)
    if not texture.reversedNormalsRed:
        normal_map[..., 0] = 1 - normal_map[..., 0]
    if not texture.reversedNormalsGreen:
        normal_map[..., 1] = 1 - normal_map[..., 1]
    imageio.imwrite(output_file, normal_map)

def threaded_process(textures):
    for i in range(0, len(textures)):
        gvars.window.write_event_value(('-NORMAL-GENERATION-', textures[i].name + ':' + str(i)), textures[i].name + ':' + str(i))
        #gvars.window['progress'].update(i + 1, len(textures))
        textureNameWithRelativePath = textures[i].path.split(os.path.join(gvars.base_path, os.path.join('pack_unziped', 'assets', 'minecraft', 'textures')))[1] + textures[i].name
        # if textures[i].name not in gvars.normals or textureNameWithRelativePath in gvars.blocks_to_ignore:
        #     continue
        if textureNameWithRelativePath in gvars.blocks_to_ignore:
            continue
        try:
            toNormal(textures[i])
        except SyntaxError:
            print("Broken png file : " + textures[i].path + textures[i].name + textures[i].ext)
        i = i+1
    #gvars.window.write_event_value(('-THREAD-', '-NORMAL-THREAD-ENDED-'), '-NORMAL-THREAD-ENDED-')

def createNormals(textures):
    #gvars.window['state'].update(value="Generating normal maps")
    gvars.window.start_thread(lambda: threaded_process(textures), ('-THREAD-', '-NORMAL-THREAD-ENDED-'))

def createNormal(texture):
    #gvars.window['state'].update(value="Generating normal maps")
    gvars.window.start_thread(lambda: threaded_process([texture]), ('-THREAD-', '-SINGLE-NORMAL-THREAD-ENDED-'))