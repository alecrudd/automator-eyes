import numpy
import cv2


def encode_to_jpeg(image):
    try:
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    except:
        return None
