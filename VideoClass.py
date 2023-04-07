import cv2

class VideoClass:
    def __init__(self, video_path, step):
        self.video = cv2.VideoCapture(video_path)
        time_marks = []

    def getNextFrame(self):
        return self.video.read()