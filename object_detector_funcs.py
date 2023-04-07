import numpy as np
import cv2
from settings import *

def sliding_window(image, step, ws):
    # slide a window across the image
    for y in range(0, image.shape[0] - ws[1], step[1]):
        for x in range(0, image.shape[1] - ws[0], step[0]):
            # yield the current window
            yield (x, y, image[y:y + ws[1], x:x + ws[0]])


def image_pyramid(image, scale=2, minSize=INPUT_SIZE):
	# yield the original image
	yield image
	# keep looping over the image pyramid
	while True:
		# compute the dimensions of the next image in the pyramid
		w = int(image.shape[0] / scale)
		h = int(image.shape[1] / scale)
		image = cv2.resize(image, (h, w))
		# if the resized image does not meet the supplied minimum
		# size, then stop constructing the pyramid
		if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
			image = cv2.resize(image, minSize)
			yield image
			break
		# yield the next image in the pyramid
		yield image

def gr_or_eq(ar1, ar2):
	if (len(ar1) != len(ar2)):
		return False
	for i in range(len(ar1)):
		if (ar1[i] < ar2[i]):
			return False
	return True
def sm_or_eq(ar1, ar2):
	if (len(ar1) != len(ar2)):
		return False
	for i in range(len(ar1)):
		if (ar1[i] > ar2[i]):
			return False
	return True

def get_overlap_class(boxes, elem):
	if (boxes == []):
		return []
	(sx, sy, ex,ey) = elem
	overlap_class = [(s1,s2,e1,e2) for (s1,s2,e1,e2) in boxes
		 if (sm_or_eq((sx,sy),(e1,e2)) and gr_or_eq((ex,ey),(e1,e2)) or
			 sm_or_eq((sx,sy),(s1,e2)) and gr_or_eq((ex,ey),(s1,e2)) or
			 sm_or_eq((sx,sy),(e1,s2)) and gr_or_eq((ex,ey),(e1,s2)) or
			 sm_or_eq((sx,sy),(s1,s2)) and gr_or_eq((ex,ey),(s1,s2)))]
	new_box = [x for x in boxes if x not in overlap_class]
	if (new_box and len(overlap_class) > 1):
		for i in overlap_class:
			overlap_class += get_overlap_class(new_box, i)
			new_box = [x for x in boxes if x not in overlap_class]
	return (overlap_class)

def merge_class_boxes(cl_boxes):
	merged_boxes = []
	for class_box in cl_boxes:
		point = [0, 0]
		side = 0
		i = 0
		for (s1,s2,e1,e2) in class_box:
			i += 1
			point[0] += s1 + e1
			point[1] += s2 + e2
			side += (s1 - e1)
		point[0] = point[0] / 2 / i
		point[1] = point[1] / 2 / i
		side = side / 2 / i
		merged_boxes.append((int(point[0] - side),
							 int(point[1] - side),
							 int(point[0] + side),
							 int(point[1] + side)))
	return (merged_boxes)


def get_overlaped_boxes(boxes):
	i = -1
	overlaped_boxes = []
	while (boxes):
		overlaped_boxes.append([])
		i+=1
		overlaped_class = get_overlap_class(boxes, boxes[0])
		overlaped_boxes[i] += (overlaped_class)
		boxes = [x for x in boxes if x not in overlaped_class]
	return overlaped_boxes
