import PySimpleGUI as sg
from PySimpleGUI import FileBrowse, ProgressBar, Slider

def initWindow():
    layout = [
        [sg.Text('Resource pack   '), sg.In(size=(50,1), enable_events=True ,key='-PACK-'), sg.FileBrowse(key='pack_path')],
        [sg.Text('Output directory '), sg.In(size=(50,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
        [sg.Text('Normal strenght  '), sg.Slider(size=(50, 10), default_value=1, range=(1, 3), resolution=0.001, orientation='h', enable_events=True, key='-NORMAL-')],
        [sg.Text('Height strenght   '), sg.Slider(size=(50, 10), default_value=0.12, range=(0.01, 0.5), resolution=0.001, orientation='h', enable_events=True, key='-HEIGHT-')],
        [sg.Checkbox('Fast specular map generation (less accurate) ', default=False, enable_events=True, key='-FAST-')],
        [sg.Text(text='', size=(50,1), key='state', visible=False)],
        [sg.ProgressBar(size=(50,5), max_value=0, key='progress', orientation='horizontal', visible=False)],
        [sg.Button('Convert', key='-CONVERT-'), sg.Button('Cancel', key='-CANCEL-'), sg.Button('Exit', key='-EXIT-', visible=False)]
    ]
    return sg.Window('PBRify', layout)
