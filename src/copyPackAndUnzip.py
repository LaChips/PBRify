import os
import shutil
import zipfile
import src.vars as gvars

def copyPackAndUnzip():
    if gvars.pack.index('.zip') == -1:
        return
    cwd = os.path.join(gvars.base_path, "pack.zip")
    shutil.copyfile(gvars.pack, cwd)
    with zipfile.ZipFile(cwd, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(gvars.base_path, 'pack_unziped'))