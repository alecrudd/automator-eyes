# camera.py

import cv2
from barcode import find_barcode


class VideoCamera(object):
    def __init__(self, num):
        self.video = cv2.VideoCapture(num)
        self.output = self.video.read()
        self.grab_started = False

    def __del__(self):
        self.video.release()

    def start_frame_grab(self):
        if(self.grab_started):
            return False
        print 'Starting the frame grabber'
        self.grab_started = True
        while self.grab_started:
            success, image = self.video.read()
            if success:
                self.output = image.copy()

    def stop_frame_grab(self):
        self.grab_started = False

    def get_frame(self):
        try:
            # success, image = self.video.read()
            # We are using Motion JPEG, but OpenCV defaults to capture raw
            # images, so we must encode it into JPEG in order to correctly
            # display video stream.
            ret, jpeg = cv2.imencode('.jpg', self.output)
            return jpeg.tobytes()
        except:
            return None

    def get_barcode(self):
        try:
            barcode = find_barcode(self.output.copy())
            ret, jpeg = cv2.imencode('.jpg', barcode)
            return jpeg.tobytes()
        except:
            return None
