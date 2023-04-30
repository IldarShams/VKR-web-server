from settings import *
import cv2;
import tensorflow as tf
from keras import datasets, layers, models, activations

# model = models.Sequential()
# model.add(tf.keras.layers.experimental.preprocessing.Resizing(224, 224, interpolation="bilinear", input_shape=(INPUT_SIZE[0], INPUT_SIZE[1], 3)))
# model.add(layers.Conv2D(96, 11, strides=4, padding='same'))
# model.add(layers.Lambda(tf.nn.local_response_normalization))
# model.add(layers.Activation('relu'))
# model.add(layers.MaxPooling2D(3, strides=2))
# model.add(layers.Conv2D(256, 5, strides=4, padding='same'))
# model.add(layers.Lambda(tf.nn.local_response_normalization))
# model.add(layers.Activation('relu'))
# model.add(layers.MaxPooling2D(3, strides=2))
# model.add(layers.Conv2D(384, 3, strides=4, padding='same'))
# model.add(layers.Activation('relu'))
# model.add(layers.Conv2D(384, 3, strides=4, padding='same'))
# model.add(layers.Activation('relu'))
# model.add(layers.Conv2D(256, 3, strides=4, padding='same'))
# model.add(layers.Activation('relu'))
# model.add(layers.Flatten())
# model.add(layers.Dense(4096, activation='relu'))
# model.add(layers.Dropout(0.5))
# model.add(layers.Dense(4096, activation='relu'))
# model.add(layers.Dropout(0.5))
# model.add(layers.Dense(2, activation='softmax'))
# model = models.Sequential()
# model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(INPUT_SIZE[0], INPUT_SIZE[1], 3)))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.Flatten())
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dense(2, activation='softmax'))
#
# cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
#                                                  save_weights_only=True,
#                                                  verbose=1)
# str = ""
# def cap_sum(x):
#     global str
#     str += x + "\n"
# model.summary(print_fn=cap_sum)
# print(str)

# print(isinstance("1", int))

# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import PySimpleGUI as sg
# import random
#
# layout=[[sg.B('Draw'),sg.B('Delete')],[sg.Canvas(key='canvas1')]]
#
# window=sg.Window("Test", layout)
#
# def draw_figure(canvas, figure):
#     figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
#     figure_canvas_agg.get_tk_widget().forget()
#     figure_canvas_agg.draw()
#     figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
#     return (figure_canvas_agg, canvas)
#
# def drawBars(x_data,y_data,barColor,legend):
#     plt.cla()
#     p1 = plt.bar(x_data, y_data, width=0.9, color=barColor)
#     plt.legend((p1[0],), (legend,))
#     plt.tight_layout()
#     fig = plt.gcf()
#     return fig
#
# l=range(1,10)
# y_data=list(l)
# x_data=list(random.sample(l,len(l)))
#
# figure_canvas_agg = None
#
# while True:
#     event, value = window.read()
#     if event == sg.WIN_CLOSED:
#         break
#     if event == 'Draw':
#         if figure_canvas_agg is not None:
#             figure_canvas_agg.get_tk_widget().delete('all')
#         (figure_canvas_agg,canvas) = draw_figure(window['canvas1'].TKCanvas, drawBars(x_data,y_data,'red','plot'))
#     if event == 'Delete':
#         if figure_canvas_agg is not None:
#             figure_canvas_agg.get_tk_widget().delete('all')
# window.close()

# def get_cam_imdexes():
#     index = 0
#     arr = []
#     while True:
#         cap = cv2.VideoCapture(index)
#         if not cap.read()[0]:
#             break
#         else:
#             arr.append(index)
#         cap.release()
#         index += 1
#     return arr
#
# i = get_cam_imdexes()
# print(i)
# cap = cv2.VideoCapture(i[0])
#
# ret = 1
# if (cap == None):
#     print('жопа')
#     exit(0)
#
# while ret:
#     ret, frame = cap.read()
#     if (ret == False):
#         break
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(0) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

#
# import fiftyone as fo
# import fiftyone.zoo as foz
#
# dataset = foz.load_zoo_dataset("quickstart")
# session = fo.launch_app(dataset)
# session.wait()
#
# from multiprocessing import Process
# import os
#
# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())
#
# def f(name):
#     info('function f')
#     print('hello', name)
#
# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()

# import sys
# from PyQt5.QtCore import pyqtSignal, QObject
# from PyQt5.QtWidgets import QMainWindow, QApplication
#
#
# class Communicate(QObject):
#
#     closeApp = pyqtSignal()
#
#
# class Example(QMainWindow):
#
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#
#     def initUI(self):
#
#         self.c = Communicate()
#         self.c.closeApp.connect(self.close)
#
#         self.setGeometry(300, 300, 290, 150)
#         self.setWindowTitle('Emit signal')
#         self.show()
#
#
#     def mousePressEvent(self, event):
#
#         self.c.closeApp.emit()
#
#
# if __name__ == '__main__':
#
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())

#  ПОТОКИ ОБЩЕНИЕ

# import sys
# from multiprocessing import Process, Queue, Pipe
#
# from PyQt5.QtCore import pyqtSignal, QThread
# from PyQt5.QtWidgets import QApplication, QLineEdit, QTextBrowser, QVBoxLayout, QDialog
#
#
# class Emitter(QThread):
#     """ Emitter waits for data from the capitalization process and emits a signal for the UI to update its text. """
#     ui_data_available = pyqtSignal(str)  # Signal indicating new UI data is available.
#
#     def __init__(self, from_process: Pipe):
#         super().__init__()
#         self.data_from_process = from_process
#
#     def run(self):
#         while True:
#             try:
#                 text = self.data_from_process.recv()
#             except EOFError:
#                 break
#             else:
#                 self.ui_data_available.emit(text.decode('utf-8'))
#
#
# class ChildProc(Process):
#     """ Process to capitalize a received string and return this over the pipe. """
#
#     def __init__(self, to_emitter: Pipe, from_mother: Queue, daemon=True):
#         super().__init__()
#         self.daemon = daemon
#         self.to_emitter = to_emitter
#         self.data_from_mother = from_mother
#
#     def run(self):
#         """ Wait for a ui_data_available on the queue and send a capitalized version of the received string to the pipe. """
#         while True:
#             text = self.data_from_mother.get()
#             self.to_emitter.send(text.upper())
#
#
# class Form(QDialog):
#     def __init__(self, child_process_queue: Queue, emitter: Emitter):
#         super().__init__()
#         self.process_queue = child_process_queue
#         self.emitter = emitter
#         self.emitter.daemon = True
#         self.emitter.start()
#
#         # ------------------------------------------------------------------------------------------------------------
#         # Create the UI
#         # -------------------------------------------------------------------------------------------------------------
#         self.browser = QTextBrowser()
#         self.lineedit = QLineEdit('Type text and press <Enter>')
#         self.lineedit.selectAll()
#         layout = QVBoxLayout()
#         layout.addWidget(self.browser)
#         layout.addWidget(self.lineedit)
#         self.setLayout(layout)
#         self.lineedit.setFocus()
#         self.setWindowTitle('Upper')
#
#         # -------------------------------------------------------------------------------------------------------------
#         # Connect signals
#         # -------------------------------------------------------------------------------------------------------------
#         # When enter is pressed on the lineedit call self.to_child
#         self.lineedit.returnPressed.connect(self.to_child)
#
#         # When the emitter has data available for the UI call the updateUI function
#         self.emitter.ui_data_available.connect(self.updateUI)
#
#     def to_child(self):
#         """ Send the text of the lineedit to the process and clear the lineedit box. """
#         self.process_queue.put(self.lineedit.text().encode('utf-8'))
#         self.lineedit.clear()
#
#     def updateUI(self, text):
#         """ Add text to the lineedit box. """
#         self.browser.append(text)
#
#
# if __name__ == '__main__':
#     # Some setup for qt
#     app = QApplication(sys.argv)
#
#     # Create the communication lines.
#     mother_pipe, child_pipe = Pipe()
#     queue = Queue()
#
#     # Instantiate (i.e. create instances of) our classes.
#     emitter = Emitter(mother_pipe)
#     child_process = ChildProc(child_pipe, queue)
#     form = Form(queue, emitter)
#
#     # Start our process.
#     child_process.start()
#
#     # Show the qt GUI and wait for it to exit.
#     form.show()
#     app.exec_()
#  ПОТОКИ ОБЩЕНИЕ


# pygrabber для поиска камер
import cv2
from pygrabber.dshow_graph import FilterGraph

graph = FilterGraph()

print(graph.get_input_devices())# list of camera device

try:
    device =graph.get_input_devices().index("Lenovo EasyCamera")

except ValueError as e:

    device = graph.get_input_devices().index("Integrated Webcam")#use default camera if the name of the camera that I want to use is not in my list

cap=cv2.VideoCapture(device)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# import cv2
#
# im = cv2.imread("C:\\Users\\User\\PycharmProjects\\CNN1\\TensorFlowYOLOv3\\IMAGES\\B0011_0001.png")
# print(im.shape)
# print(im.shape[0])
# print(im.shape[1])

