import os
import shutil

def repackTextures(window, output_filename, directory, base_path):
    window['state'].update(value="repacking "+output_filename+"" in "+directory")
    if (os.path.isfile(directory + "/" + output_filename)):
        os.remove(directory + "/" + output_filename, 'zip')
    shutil.make_archive(directory + "/" + output_filename, 'zip', os.path.join(base_path, 'pack_unziped'))