import matplotlib.pyplot as plt
import numpy
import os
import PIL
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import Sequential
from keras import datasets, layers, models
from settings import *
from object_detector_funcs import *
import cv2


class cnn_class:

    def __init__(self):
        self.cnn = None
        self.ss = None

    def process_frame(self, frame):
        # (H, W, RGB) = frame.shape
        #
        # self.ss.setBaseImage(frame)
        # self.ss.switchToSelectiveSearchFast(base_k =1200, inc_k=600)
        # print("    Выделение зон...")
        # rects = self.ss.process()
        # print("    Выделение зон закончено...")
        # proposals = []
        # locs = []
        # for (x, y, w, h) in rects:
        #     if w / float(W) < 0.1 or h / float(H) < 0.1:
        #         continue
        #     roi = frame[y:y + h, x:x + w]
        #     roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        #     roi = cv2.resize(roi, INPUT_SIZE)
        #     proposals.append(roi[np.newaxis, ...])
        #     locs.append((x, y, x + w, y + h))
        # rects = None
        # preds = []
        # print("    Создание dataset...")
        # dataset = tf.data.Dataset.from_tensor_slices(proposals)
        # proposals = None
        # print("    Создание dataset окончено...")
        #
        # print("     обработка зон в cnn...")
        # preds = self.cnn.predict(dataset)
        # # for pic in proposals:
        # #     preds.append(self.cnn.predict(pic, verbose=0))
        # print("     обработка зон в cnn окончено...")
        #
        # boxes = []
        #
        # for i in range(len(preds)):
        #     if preds[i][0] >= MIN_ACCUR:
        #         boxes.append(locs[i])
        rois = []
        locs = []
        (H, W, RGB) = frame.shape
        pyramid = image_pyramid(frame)
        for image in pyramid:

            scale = W / float(image.shape[1])

            for (x, y, roiOrig) in sliding_window(image, STEP, ROI_SIZE):
                x = int(x * scale)
                y = int(y * scale)
                w = int(ROI_SIZE[0] * scale)
                h = int(ROI_SIZE[1] * scale)

                roi = cv2.resize(roiOrig, INPUT_SIZE)
                rois.append(roi[np.newaxis])
                locs.append((x, y, x + w, y + h))
        dataset = tf.data.Dataset.from_tensor_slices(rois)
        preds = self.cnn.predict(dataset)
        boxes = []
        for i in range(len(preds)):
            if preds[i][0] >= MIN_ACCUR:
                boxes.append(locs[i])
        boxes = get_overlaped_boxes(boxes)
        boxes = merge_class_boxes(boxes)
        for (startX, startY, endX, endY) in boxes:
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          (0, 255, 0), 2)
        return boxes

    def model_init(self):
        self.cnn = create_model()
        self.cnn.load_weights(checkpoint_path)
        self.ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

    def getNextFrame(self):
        return self.video.read()
