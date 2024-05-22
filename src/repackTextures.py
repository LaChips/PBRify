import os
import shutil
import src.vars as gvars
import threading

#def thread_function(path):
#    shutil.make_archive(gvars.directory + "/" + path, 'zip', os.path.join(gvars.base_path, 'pack_unziped'))
#    gvars.done = True

def repackTextures(output_filename):
    print("repacking "+output_filename+" in "+gvars.directory)
    gvars.window['state'].update(value="repacking "+output_filename+" in "+gvars.directory)
    if (os.path.isfile(gvars.directory + "/" + output_filename)):
        os.remove(gvars.directory + "/" + output_filename, 'zip')
    shutil.make_archive(gvars.directory + "/" + output_filename, 'zip', os.path.join(gvars.base_path, 'pack_unziped'))