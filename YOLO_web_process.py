import anvil.server
import cv2
import os
from TensorFlowYOLOv3.yolov3.utils import *  #utils # import  detect_image, detect_image_for_vid, detect_realtime, detect_video, Load_Yolo_model, detect_video_realtime_mp
from TensorFlowYOLOv3.yolov3.configs import *
anvil.server.connect("server_UEMV3BW3LSDTQKDRMBFZRZKQ-VKPUFIU4RXBWF7MK")

yolo = Load_Yolo_model()

@anvil.server.callable
def process_image(image):
    try:
        # print(image)
        print(type(image))
        im = np.asarray(image, dtype="uint8")
        im = cv2.imdecode(im, cv2.IMREAD_COLOR)
        im = cv2.cvtCOLOR(im, cv2.BGR2RGB)
        bbox = detect_image(yolo, im, "./IMAGES/plate_1_detect.jpg", input_size=YOLO_INPUT_SIZE,
                             show=True, CLASSES=TRAIN_CLASSES, rectangle_colors=(255, 0, 0))
    except Exception as e:
        print(e)


anvil.server.wait_forever()
