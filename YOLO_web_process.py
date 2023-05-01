import anvil.server
import cv2
import os

import numpy as np

from TensorFlowYOLOv3.yolov3.utils import *  #utils # import  detect_image, detect_image_for_vid, detect_realtime, detect_video, Load_Yolo_model, detect_video_realtime_mp
from TensorFlowYOLOv3.yolov3.configs import *
anvil.server.connect("server_UEMV3BW3LSDTQKDRMBFZRZKQ-VKPUFIU4RXBWF7MK")
# current_image = ""
yolo = Load_Yolo_model()
print("сервер готво к работе")

# @anvil.server.callable
# def get_chunk(chunk):
#     global current_image
#     current_image = current_image + chunk
@anvil.server.callable
def process_image(blob, dtype):
    try:

        # global current_image
        image = blob.get_bytes()
        print("YOLO: Изображение получено")
        # print(image)
        print(type(image))
        im = np.frombuffer(image, dtype="uint8")
        im = cv2.imdecode(im, cv2.IMREAD_COLOR)
        print("YOLO: определеяем объекты")
        bboxes = detect_image_for_vid(yolo, im, "./IMAGES/plate_1_detect.jpg", input_size=YOLO_INPUT_SIZE,
                             show=True, CLASSES=TRAIN_CLASSES, rectangle_colors=(255, 0, 0))
        print("YOLO: результат получен")
        return bboxes
    except Exception as e:
        print(e)


anvil.server.wait_forever()
