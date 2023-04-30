from PyQt6.QtCore import QThread, pyqtSignal
from multiprocessing import Pipe

class Emitter(QThread):

    image_available = pyqtSignal()

    def __init__(self, from_yolo_process : Pipe):
        super().__init__()
        self.yolo_data = from_yolo_process

    def run(self):
        while True:
            try:
                signal = self.yolo_data.recv()
                print("Emitter: Получен сигнал от йоло:", signal)
            except EOFError:
                print("Emitter: Что то пошло не так")
            else:
                print("Emitter: Отправка сигнала окну")
                self.image_available.emit()


