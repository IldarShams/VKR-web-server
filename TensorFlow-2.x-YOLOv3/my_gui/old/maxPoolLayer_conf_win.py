import PySimpleGUI as sg
from messges import *

def maxPool_layer_conf_win(first_layer):
    input_size1 = []
    input_size2 = []
    if (first_layer):
        input_size1 = [sg.Text('Размер входного изображения')]
        input_size2 = [sg.Input(k='-InputX-'), sg.Input(k='-InputY-')]
    layout2 = [
        [
            sg.Col([[sg.Text('Выборка')],
                    [sg.Text('Шаг')],
                    [sg.Text('Padding')],
                    input_size1]),
            sg.Col([[sg.Input("2", k="-PoolX-"),sg.Input("2", k="-PoolY-")],
                    [sg.Input("1", k="-Stride-")],
                    [sg.Combo(["same", "valid"],"same",k="-Padding-")],
                    input_size2])
        ],
        [sg.Button('Ok', k='-ConvOk-')]
    ]
    win = sg.Window('Подвыборка',layout2,keep_on_top=True)
    return win

def maxPool_layer_conf_check_input(firstLayer, valuesConv, model):
    if (any([v=='' for v in valuesConv.values()])):
        sg.popup_error(NOT_ALL_FIELDS_ARE_FILLED, keep_on_top=True)
        return False
    try:
        if (int(valuesConv['-Stride-']) <= 0):
            raise('отрицательный шаг')
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
