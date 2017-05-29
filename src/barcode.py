'''
 adapted from
 http://www.pyimagesearch.com/2014/11/24/detecting-barcodes-images-python-opencv/
'''

import numpy as np
import cv2


def find_barcode(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # compute the Scharr gradient magnitude representation of the images
    # in both the x and y direction
    gradX = cv2.Sobel(grey, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(grey, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # blur and threshold the image
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations=5)
    closed = cv2.dilate(closed, None, iterations=5)

    # find the contours in the thresholded image, then sort the contours
    # by their area, keeping only the largest one

    im2, contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return img

    c = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    if cv2.contourArea(c) < 1000:
        return img

    rect = cv2.minAreaRect(c)
    newrect = (rect[0], (rect[1][0]+30, rect[1][1]+30), rect[2])
    box = cv2.boxPoints(newrect)
    box = np.int0(box)

    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    return img
