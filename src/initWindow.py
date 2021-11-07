import PySimpleGUI as sg
from PySimpleGUI import FileBrowse, ProgressBar

def initWindow():
    layout = [
        [sg.Text('Resource pack   '), sg.In(size=(50,1), enable_events=True ,key='-PACK-'), sg.FileBrowse(key='pack_path')],
        [sg.Text('Output directory '), sg.In(size=(50,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
        [sg.Text(text='', size=(50,1), key='state', visible=False)],
        [sg.ProgressBar(size=(50,5), max_value=0, key='progress', orientation='horizontal', visible=False)],
        [sg.Button('Convert'), sg.Button('Cancel')]
    ]
    return sg.Window('PBRify', layout)
