import os
import shutil
import zipfile

def copyPackAndUnzip(path, base_path):
    if path.index('.zip') == -1:
        return
    cwd = os.path.join(base_path, "pack.zip")
    shutil.copyfile(path, cwd)
    with zipfile.ZipFile(cwd, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(base_path, 'pack_unziped'))