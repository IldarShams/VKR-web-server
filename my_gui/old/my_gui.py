import PySimpleGUI as sg
from settings import *
import tensorflow as tf
from keras import datasets, layers, models
from convLayer_conf_win import *

use_custom_titlebar = False
first_layer = False
model_sum = ""
model= None

def make_window(theme=None):

    sg.theme(theme)
    setting_panes = [
        sg.Pane([
            sg.Column([[
                        sg.Column([[sg.Text('Тренировочные данные')],[sg.Text('Проверочные данные')],[sg.Text('Веса')]]),
                       sg.Column([[sg.Input('Путь')],[sg.Input('Путь')],[sg.Input('Путь')]]),
                       sg.Column([[sg.FileBrowse('Browse')], [sg.FileBrowse('Browse')], [sg.FileBrowse('Browse')]])
                    ]]),
            sg.Column([[
                sg.Column([[sg.Text('ROI')], [sg.Text('STEP')], [sg.Text('ЧТО то0')]]),
                sg.Column([[sg.Input('x')], [sg.Input('x')], [sg.Input('что то1')]]),
                sg.Column([[sg.Input('y')], [sg.Input('y')], [sg.FileBrowse('что то2')]])
            ]])
        ], expand_x=True,expand_y=True, show_handle=False, background_color="Black")
    ]
    model_panes = [
        sg.Pane([
            sg.Column([

                [sg.Button('Новая модель', k="-NewModel-"), sg.Input("Имя")],
                [
                    sg.Column([[sg.Button('Сохранить')], [sg.Button('Загрузить модель')], [sg.Button('Загрузить веса')]]),
                    sg.Column([[sg.Input()], [sg.Input()], [sg.Input()]]),
                    sg.Column([[sg.FileBrowse('Brows')], [sg.FileBrowse('Brows')], [sg.FileBrowse('Brows')]])
                ]
           ]),
            sg.Column([

                [sg.Text('Слои')],
                [
                    sg.Combo(["Свёртка", "Подвыборка", "Выравнивание", "Полносвяный слой"], k="-ChooseLayer-"),
                    sg.Button("Добавить слой", k="-AddLayer-")
                ],
                [sg.Text("Количество параметров:"), sg.Text()]
            ])
        ], expand_x=True,expand_y=True, show_handle=False, background_color="Black")

    ]
    settings_tab = sg.Tab('Настройки',[setting_panes])
    learning_tab = sg.Tab('Обучение', [[]])
    model_conf_tab = sg.Tab('Модель', [model_panes])

    layout_l = [[]]
    layout_r  = [   [ sg.TabGroup([ [settings_tab, learning_tab, model_conf_tab] ]) ]   ]

    layout = [[sg.MenubarCustom([['File', ['Exit']], ['Edit', ['Edit Me', ]]],  k='-CUST MENUBAR-',p=0)] if use_custom_titlebar else [sg.Menu([['File', ['Exit']], ['Edit', ['Edit Me', ]]],  k='-CUST MENUBAR-',p=0)],
              [sg.Col(layout_l), sg.Col(layout_r)]]

    window = sg.Window('The PySimpleGUI Element List', layout, finalize=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=True, use_custom_titlebar=use_custom_titlebar)
    return window



def cap_sum(x):
    global model_sum
    model_sum += x + "\n"
# Start of the program...
window = make_window()
changes_in_model = False
while True:
    event, values = window.read()
    sg.popup(event, values, keep_on_top=True)                 # show the results of the read in a popup Window
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    # if values['-NewModel-'] != sg.theme():
    #     sg.theme(values['-COMBO-'])
    #     window.close()
    #     window = make_window()
    if event == '-AddLayer-':
        if (model == None):
            sg.popup_error(MODEL_IS_NONE, keep_on_top=True)
            continue
        layer = values['-ChooseLayer-']
        if (layer == "Свёртка"):
            convWin = conv_layer_conf_win(first_layer)
            eventConv, valuesConv = convWin.read()
            sg.popup(eventConv, valuesConv, keep_on_top=True)
            if (eventConv == '-ConvOk-'):
                check_res = conv_layer_conf_check_input(first_layer, valuesConv, model)
                if (not check_res):
                    convWin.close()
                    continue
                model.add(
                    layers.Conv2D(
                        int(valuesConv['-Channels-']),
                        int(valuesConv['-Kernel-']),
                        input_shape=(int(valuesConv['-InputX-']),
                        int(valuesConv['-InputY-']),3))
                )
                convWin.close()
                model.summary(print_fn=cap_sum)
                sg.popup_ok(model_sum, keep_on_top=True)
    if event == '-NewModel-':
        if (model != None and changes_in_model == True):
            res = sg.popup_yes_no('Предыдущая модель не сохранена, продолжить?', keep_on_top=True)
            if (res == 'No'):
                continue
        model = models.Sequential()
        changes_in_model = True
        first_layer = True
window.close()
