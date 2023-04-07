import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import Sequential
from keras import datasets, layers, models
from settings import *
from object_detector_funcs import *

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']
rois = []
locs = []

# test = cv2.imread("C:\\Users\\User\\Desktop\\frogs\\data\\_object\\0.jpg")
test = cv2.imread("C:\\Users\\User\\Desktop\\test_im2.png")


#test = cv2.resize(test, (test.shape[1]*4, test.shape[0]*4))

# (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
model = create_model()
model.load_weights(checkpoint_path)
(H,W,RGB) = test.shape

test = cv2.cvtColor(test, cv2.COLOR_BGR2RGB)

for image in image_pyramid(test):

    scale = W / float(image.shape[1])

    for (x, y, roiOrig) in sliding_window(image, STEP, ROI_SIZE):

        x = int(x * scale)
        y = int(y * scale)
        w = int(ROI_SIZE[0] * scale)
        h = int(ROI_SIZE[1] * scale)

        roi = cv2.resize(roiOrig, INPUT_SIZE)
        rois.append(roi[np.newaxis,...])
        locs.append((x, y, x + w, y + h))

dataset = tf.data.Dataset.from_tensor_slices(rois)
#
# for element in dataset:
#     print(element)
preds = model.predict(dataset)
# print(preds.shape)
# print(len(locs))

boxes = []
for i in range(len(preds)):
    # grab the prediction information for the current ROI

    # filter out weak detections by ensuring the predicted probability
    # is greater than the minimum probability
    if preds[i][0] >= MIN_ACCUR:
        # grab the bounding box associated with the prediction and
        # convert the coordinates
        boxes.append(locs[i])
        # print(preds[i][1])
        # grab the list of predictions for the label and add the
        # bounding box and probability to the list
# boxes = get_overlaped_boxes(boxes)
# boxes = merge_class_boxes(boxes)
test2 = test.copy()
for (startX, startY, endX, endY) in boxes:
    # draw the bounding box and label on the image
    cv2.rectangle(test, (startX, startY), (endX, endY),
        (0, 255, 0), 2)
cv2.imshow('test', cv2.resize(test, (720,480)))
cv2.waitKey(0) & 0xff
boxes = get_overlaped_boxes(boxes)
boxes = merge_class_boxes(boxes)
for (startX, startY, endX, endY) in boxes:
    # draw the bounding box and label on the image
    cv2.rectangle(test2, (startX, startY), (endX, endY),
        (0, 255, 0), 2)
cv2.imshow('test', cv2.resize(test2, (720,480)))
cv2.waitKey(0) & 0xff


