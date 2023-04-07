import PySimpleGUI as sg
from messges import *

def conv_layer_conf_win(first_layer):
    input_size1 = []
    input_size2 = []
    if (first_layer):
        input_size1 = [sg.Text('Размер входного изображения')]
        input_size2 = [sg.Input(k='-InputX-'), sg.Input(k='-InputY-')]
    layout2 = [
        [
            sg.Col([[sg.Text('Количество выходных каналов')],[sg.Text('Ядро свёртки')],input_size1]),
            sg.Col([[sg.Input(k="-Channels-")], [sg.Input(k="-Kernel-")], input_size2])
        ],
        [sg.Button('Ok', k='-ConvOk-')]
    ]
    win = sg.Window('Свёртка',layout2,keep_on_top=True)
    return win

def conv_layer_conf_check_input(firstLayer, valuesConv, model):
    if (any([v=='' for v in valuesConv.values()])):
        sg.popup_error(NOT_ALL_FIELDS_ARE_FILLED, keep_on_top=True)
        return False
    try:
        if (int(valuesConv['-Channels-']) <= 0):
            raise('отрицательное число выходных каналов')
    except Exception as e:
        sg.popup_error(BAD_FORMAT + str(e), keep_on_top=True)
        return False
    try:
        if (int(valuesConv['-Kernel-']) <= 0):
            raise('отрицательное число')
    except Exception as e:
        sg.popup_error(BAD_FORMAT + str(e), keep_on_top=True)
        return False
    if (firstLayer):
        try:
            if (int(valuesConv['-InputX-']) <= 0 or int(valuesConv['-InputY-']) <= 0):
                raise('отрицательное число')
        except Exception as e:
            sg.popup_error(BAD_FORMAT + str(e), keep_on_top=True)
            return False
    return True
