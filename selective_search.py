import argparse
import random
import keras
import numpy as np
import time
import cv2
from settings import *
from object_detector_funcs import *
from keras.applications import ResNet50
from keras.applications import imagenet_utils


method = "fast"

test = cv2.imread("C:\\Users\\User\\Desktop\\test_im6.png")
(H,W,RGB) = test.shape

ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
ss.setBaseImage(test)
if method == "fast":
	print("[INFO] using *fast* selective search")
	ss.switchToSelectiveSearchFast(base_k=600,inc_k=10)
else:
	print("[INFO] using *quality* selective search")
	ss.switchToSelectiveSearchQuality()

start = time.time()
rects = ss.process()
end = time.time()
print("Время поиска боксов:" + str(end - start))
# proposals = []
# locs = []
# model = create_model()
# model.load_weights(checkpoint_path)
# for (x, y, w, h) in rects:
# 	if w / float(W) < 0.1 or h / float(H) < 0.1:
# 		continue
# 	roi = test[y:y + h, x:x + w]
# 	roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
# 	roi = cv2.resize(roi, INPUT_SIZE)
# 	proposals.append(roi[np.newaxis, ...])
# 	locs.append((x, y, x + w, y + h))

# preds = []
# for pic in proposals:
# 	preds.append(model.predict(pic,verbose = 0))


boxes = []
for (sx, sy,w,h) in rects:
	boxes.append((sx,sy,sx+w, sy+h))

# for i in range(len(preds)):
#     if preds[i][0][0] >= MIN_ACCUR:
#         boxes.append(locs[i])

# test2 = test.copy()
# for (startX, startY, endX, endY) in boxes:
#     # draw the bounding box and label on the image
#     cv2.rectangle(test, (startX, startY), (endX, endY),
#         (0, 255, 0), 2)
# cv2.imshow('test', cv2.resize(test, (720,480)))
# cv2.waitKey(0) & 0xff
# boxes = get_overlaped_boxes(boxes)
# boxes = merge_class_boxes(boxes)
# for (startX, startY, endX, endY) in boxes:
#     # draw the bounding box and label on the image
#     cv2.rectangle(test2, (startX, startY), (endX, endY),
#         (0, 255, 0), 2)
# cv2.imshow('test', cv2.resize(test2, (720,480)))
# cv2.waitKey(0) & 0xff

print("Найдено боксов:" + str(len(rects)))
for i in range(0, len(rects), 100):
	# clone the original image so we can draw on it
	output = test.copy()
	# loop over the current subset of region proposals
	for (x, y, w, h) in rects[i:i + 100]:
		# draw the region proposal bounding box on the image
		color = [random.randint(0, 255) for j in range(0, 3)]
		cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
	# show the output image
	cv2.imshow("Output", output)
	key = cv2.waitKey(0) & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break


