import os
import shutil
import json
import zipfile
import threading
import PySimpleGUI as sg
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QPushButton, QListWidget, QListWidgetItem, QGridLayout, QLineEdit
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from typing import List
from src.texture import Texture
from src.fetchTextures import TextureFetcher
from src.createNormalsMaps import createNormals
from src.createHeightMaps import createHeightMaps
from src.createSpecularMaps import createSpecularMaps
from src.vars import Config, AppState, UNZIP_DIR

class Converter:

    def __init__(self, config : Config, app : AppState):
        self.config = config
        self.app = app
        self.texture_window = None
        self.cancelled = True
        self.normals = []
        self.speculars = []
        self.textures_data = None

    def start(self):
        print("configuration :", self.config)
        self.prepareEnvironment()

        textureFetcher = TextureFetcher(self)
        textureSelector = TextureSelector(textureFetcher.getTextures(), self.config)
        cancelled, updated_textures = textureSelector.initTextureSelection()

        if cancelled:
            return

        # Use the updated textures list from now on
        self.normals = [tex.name for tex in updated_textures if tex.generate_normal]
        self.speculars = [tex.name for tex in updated_textures if tex.generate_specular]

        normal_textures = [tex for tex in updated_textures if tex.generate_normal]
        specular_textures = [tex for tex in updated_textures if tex.generate_specular]

        createNormals(normal_textures, self)
        createHeightMaps(normal_textures, self)
        createSpecularMaps(specular_textures, self)

        self.repackTextures(self.config.pack.split('/')[-1].split('.zip')[0] + "_PBR")

    def prepareEnvironment(self):
        if os.path.isfile(os.path.join(self.config.base_path, 'pack.zip')):
            os.remove(os.path.join(self.config.base_path, 'pack.zip'))
        if os.path.isdir(os.path.join(self.config.base_path, UNZIP_DIR)):
            shutil.rmtree(os.path.join(self.config.base_path, UNZIP_DIR), ignore_errors=True)

        with open(os.path.join(self.config.base_path, 'lib/textures_data.json'), 'r') as json_file:
            self.textures_data = json.loads(json_file.read())

        self.copyPackAndUnzip()
        self.app.window['state'].update(visible=True)
        self.app.window['progress'].update(visible=True)


    def copyPackAndUnzip(self):
        if self.config.pack.index('.zip') == -1:
            return
        cwd = os.path.join(self.config.base_path, "pack.zip")
        shutil.copyfile(self.config.pack, cwd)
        with zipfile.ZipFile(cwd, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(self.config.base_path, UNZIP_DIR))

    def repackTextures(self, output_filename):
        self.app.window['state'].update(value="repacking "+output_filename+" in "+ self.config.directory)
        if (os.path.isfile(self.config.directory + "/" + output_filename)):
            os.remove(self.config.directory + "/" + output_filename, 'zip')
        x = threading.Thread(target=self.thread_function, args=(output_filename,))
        x.start()

    def thread_function(self, path):
        shutil.make_archive(self.config.directory + "/" + path, 'zip', os.path.join(self.config.base_path, UNZIP_DIR))
        self.app.done = True

class TextureSelector:

    def __init__(self, textures, config : Config) -> None:
        self.app = QApplication([])
        self.window = QWidget()
        self.textures = textures
        self.updating_checkboxes = False  # Flag to control updates
        self.speculars : List[str] = config.speculars
        self.normals : List[str] = config.normals

    # Shows all the textures found in a resource pack, to let the user select what textures to convert, textures found in the normals list will automatically be selected
    def initTextureSelection(self):
        self.window.setWindowTitle('Select textures to convert')
        self.window.resize(800, 400)

        layout = QVBoxLayout()

        # Add filter line edit
        self.filter_line_edit = QLineEdit()
        self.filter_line_edit.setPlaceholderText("Filter textures by name...")
        self.filter_line_edit.textChanged.connect(self.filter_textures)
        layout.addWidget(self.filter_line_edit)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        layout.addWidget(self.list_widget, 1)

        self.texture_widgets = {}  # To store references to widgets for filtering
        for texture in self.textures:
            item = QListWidgetItem()
            widget = self.createTextureWidget(texture, texture.name in self.normals, texture.name in self.speculars)
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())
            self.texture_widgets[texture.name] = (item, widget)  # Store item and widget for filtering

        # Action buttons for normals and speculars
        normals_button = QPushButton('Set Normals for Selected')
        speculars_button = QPushButton('Set Speculars for Selected')
        normals_button.clicked.connect(lambda: self.update_selected('normals'))
        speculars_button.clicked.connect(lambda: self.update_selected('speculars'))
        button_layout = QHBoxLayout()
        button_layout.addWidget(normals_button)
        button_layout.addWidget(speculars_button)
        layout.addLayout(button_layout)

        # Confirm and Cancel buttons
        confirm_button = QPushButton('Confirm')
        cancel_button = QPushButton('Cancel')
        confirm_button.clicked.connect(self.on_convert_clicked)
        cancel_button.clicked.connect(self.on_cancel_clicked)
        button_layout = QHBoxLayout()
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.window.setLayout(layout)
        self.window.show()
        self.app.exec()

        return self.cancelled, self.getUpdatedTextureList()


    def filter_textures(self):
        filter_text = self.filter_line_edit.text().lower()
        for name, (item, widget) in self.texture_widgets.items():
            if filter_text in name.lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def createTextureWidget(self, texture, generate_normals, generate_speculars):
        widget = QWidget()
        grid = QGridLayout(widget)
        widget.normals_checkbox = QCheckBox('Normals')
        widget.speculars_checkbox = QCheckBox('Speculars')
        widget.texture = texture

        pixmap = QPixmap(texture.full_path)
        label = QLabel()
        label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        grid.addWidget(label, 0, 0, 1, 1)
        name_label = QLabel(texture.name)
        grid.addWidget(name_label, 0, 1, 1, 1)

        widget.normals_checkbox.setChecked(generate_normals)
        widget.normals_checkbox.stateChanged.connect(lambda state, t=texture: self.update_normals(t, state))

        widget.speculars_checkbox.setChecked(generate_speculars)
        widget.speculars_checkbox.stateChanged.connect(lambda state, t=texture: self.update_speculars(t, state))

        grid.addWidget(widget.normals_checkbox, 0, 2, 1, 1)
        grid.addWidget(widget.speculars_checkbox, 0, 3, 1, 1)

        return widget

    def update_normals(self, texture: Texture, state):

        generate_normal = state == Qt.CheckState.Checked

        if generate_normal:
            self.normals.append(texture.name)
        elif texture.name in self.normals:
            self.normals.remove(texture.name)


    def update_speculars(self, texture: Texture, state):

        generate_specular = state == Qt.CheckState.Checked

        if generate_specular:
            self.speculars.append(texture.name)
        elif texture.name in self.speculars:
            self.speculars.remove(texture.name)

    def update_selected(self, attribute):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return

        self.updating_checkboxes = True
        # Get the check state for the first item in the list, will toggle all items to this state
        first_widget = self.list_widget.itemWidget(selected_items[0])
        target_state = first_widget.normals_checkbox.isChecked() if attribute == 'normals' else first_widget.speculars_checkbox.isChecked()

        for item in selected_items:
            widget = self.list_widget.itemWidget(item)
            checkbox = widget.normals_checkbox if attribute == 'normals' else widget.speculars_checkbox
            checkbox.setChecked(target_state)  # Set state based on the target_state, not toggle

            # Update the internal list based on this state
            texture_name = widget.texture.name
            texture_list = self.normals if attribute == 'normals' else self.speculars
            if target_state:
                if texture_name not in texture_list:
                    texture_list.append(texture_name)
            else:
                if texture_name in texture_list:
                    texture_list.remove(texture_name)

        self.updating_checkboxes = False


    def on_convert_clicked(self):
        print('Conversion started...')
        self.cancelled = False
        self.window.close()

    def on_cancel_clicked(self):
        self.cancelled = True
        self.window.close()

    def getUpdatedTextureList(self) -> List[Texture]:

        outTextures : List[Texture] = []

        for texture in self.textures:
            if texture.name in self.normals:
                texture.generate_normal = True
            else:
                texture.generate_normal = False

            if texture.name in self.speculars:
                texture.generate_specular = True
            else:
                texture.generate_specular = False

            outTextures.append(texture)

        return outTextures