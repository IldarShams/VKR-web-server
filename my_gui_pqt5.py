from my_gui.MainWindowClass import *
from my_gui.MessageWindowClass import *
from YOLO_process import *
from my_gui.Emitter import *
from multiprocessing import Pipe


# import sys
# import os
# os.system("cd")





if __name__ == "__main__":
    mother_pipe, child_pipe = Pipe()
    queue_form_win_to_yolo = Queue()
    queue_from_yolo_to_win = Queue()
    lock = Lock()

    app = QApplication(sys.argv)


    # запуск процесса нейронки
    emitter = Emitter(mother_pipe)
    # yolo = YoloProcess(queue_form_win_to_yolo, queue_from_yolo_to_win, child_pipe, lock)
    # yolo.start()

    window = MainWindow(queue_form_win_to_yolo, queue_from_yolo_to_win, emitter, lock)
    window.show()
    app.exec()