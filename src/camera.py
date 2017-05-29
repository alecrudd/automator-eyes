# camera.py

import cv2
from barcode import find_barcode


class VideoCamera(object):
    def __init__(self, num):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(num)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_barcode(self):
        success, image = self.video.read()
        barcode = find_barcode(image)
        ret, jpeg = cv2.imencode('.jpg', barcode)
        return jpeg.tobytes()
