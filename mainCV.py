import string
import time;
from object_detector_funcs import *
import numpy as np
from cnn import *
import cv2

neiro = cnn_class()
neiro.model_init()

cap = cv2.VideoCapture("C:\\Users\\User\\Desktop\\test2_smol2.mp4")
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output2.avi',fourcc, 30, videoFormat, True)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_number = -1
counter = 0
matmean = [0, 0]
ret = 1
time_start = time.time()

#
# test = cv2.imread("C:\\Users\\User\\Desktop\\frog.jpg")
# print(test[0][0])

# if (test.all(None)):
#     print('жепа')
# else:
#     for f in sliding_window(test, 100, (100, 100)):
#         print(f[2])
#         cv2.imshow('frame', f[2])
#         cv2.waitKey()

# for im in image_pyramid(test, 1.5, (100, 100)):
#     cv2.imshow('frame', im)
#     cv2.waitKey()
if (cap == None):
    print('жопа')
    exit(0)
boxes = []
while ret:
    frame_number = (frame_number + 1) % FRAME_STEP
    ret, frame = cap.read()
    if (ret == False):
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    counter += 1
    frame = cv2.putText(frame, str(round(counter / 30 / 60)) + ":" + str(round(counter / 30 % 60)),
                        (50, 50), 1, 1.0, (255, 255, 255), 2, cv2.FILLED, 0)
    if frame_number == FRAME_STEP - 1:
        print("Обработка фрейма...")
        (boxes) = neiro.process_frame(frame)
        print("Обработка фрейма окончена...")
        time_end = time.time()
        time_span = time_end - time_start
        time_start = time_end
        matmean[0] = (matmean[0] * matmean[1] + time_span) / (FRAME_STEP + matmean[1])
        matmean[1] += FRAME_STEP
        print(str(round(matmean[0]*length/60)) +":" + str(round(matmean[0]*length%60)))
        print("Оставшееся кол-во фреймов:" +  str(total - counter) + "; "
              + "Примерное время до конца:" +  str(round(matmean[0] * (total - counter) /60))
              + ":" + str(round(matmean[0] * (total - counter) % 60)))
    for (startX, startY, endX, endY) in boxes:
        cv2.rectangle(frame, (startX, startY), (endX, endY),
                      (0, 255, 0), 2)
    frame = cv2.resize(frame, videoFormat)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    out.write(frame)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('frame',frame)
    # if cv2.waitKey(0) & 0xFF == ord('q'):
    #     break

cap.release()
out.release()
cv2.destroyAllWindows()
