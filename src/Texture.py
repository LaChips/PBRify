import os
from PIL import Image

class Texture:
    def __init__(self, path, name, ext):
        self.path = path
        self.name = name
        self.extension = ext
        self.full_path = f"{path}{name}{ext}"
        self.thumbnail_dir = os.path.join(path, 'thumbnails')
        self.thumbnail_path = os.path.join(self.thumbnail_dir, f"{name}_thumb{ext}")
        self.ext = ext

    # Create a thumbnail of the texture to display in GUI
    def create_thumbnail(self, size=(64, 64)):
        if not os.path.exists(self.thumbnail_dir):
            os.makedirs(self.thumbnail_dir)  # Create the thumbnails directory if it does not exist
        try:
            img = Image.open(self.full_path)
            img.thumbnail(size)
            img.save(self.thumbnail_path)
        except Exception as e:
            print(f"Failed to create thumbnail for {self.full_path}: {e}")
