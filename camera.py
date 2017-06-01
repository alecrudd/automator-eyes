'''
camera.py
'''

import cv2
import sys
import threading
from barcode import find_barcode


class VideoCamera(object):
    def __init__(self, num):
        try:
            self.video = cv2.VideoCapture(num)
            self.output = self.video.read()[1]
            self.grab_started = False
        except:
            pass

    def is_open(self):
        return self.video.isOpened()

    def __del__(self):
        self.video.release()

    def grab_frames(self):
        while self.grab_started:
            success, image = self.video.read()
            if success:
                self.output = image.copy()

    def start_frame_grab(self):
        if(self.grab_started):
            return False
        print 'Starting the frame grabber'
        self.grab_started = True
        grabber_thread = threading.Thread(target=self.grab_frames)
        grabber_thread.start()

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
            print 'Error encoding frame:', sys.exc_info()[0]
            return None

    def get_barcode_frame(self):
        try:
            barcode = find_barcode(self.output.copy())
            if(barcode is None):
                print 'barcode empty'
            ret, jpeg = cv2.imencode('.jpg', barcode.copy())
            return jpeg.tobytes()
        except:
            print 'Error encoding frame:', sys.exc_info()[0]
            return None
