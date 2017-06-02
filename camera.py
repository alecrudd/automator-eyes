'''
camera.py
'''
import numpy
import cv2
import sys
import threading
from barcode import find_barcode
import glyphdetector as gd

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

    def grab_frames(self, rotation, zoom, crop):
        while self.grab_started:
            success, image = self.video.read()
            if success:
                resized_image = cv2.resize(image, None, fx=zoom, fy=zoom)
                (h, w) = resized_image.shape[:2]
                center = (w / 2, h / 2)

                rot_mat = cv2.getRotationMatrix2D(center, rotation, 1)
                result = cv2.warpAffine(resized_image, rot_mat, (w, h))
                # if crop is None:
                #     self.output = result.copy()
                # else:
                cropped = result[crop[1]:h-crop[1], crop[0]:w-crop[0]]
                self.output = cropped.copy()

    def start_frame_grab(self, rotation=0, zoom=1, crop=(0, 0)):
        if(self.grab_started):
            return False
        print 'Starting the frame grabber'
        self.grab_started = True
        grabber_thread = threading.Thread(target=self.grab_frames,
                                          args=(rotation, zoom, crop,))
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
            ret, jpeg = cv2.imencode('.jpg', barcode)
            return jpeg.tobytes()
        except:
            return None

    def get_glyph_frame(self):
        glyph = gd.find_glyph(self.output.copy())
        if glyph is not None:
            ret, jpeg = cv2.imencode('.jpg', glyph)
            return jpeg.tobytes()
        return None
