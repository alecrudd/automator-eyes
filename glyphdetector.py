import numpy
import cv2
from glyphhelpers import *

QUADRILATERAL_POINTS = 4
SHAPE_RESIZE = 100.0
BLACK_THRESHOLD = 100
WHITE_THRESHOLD = 155


def find_glyph(image):
        # Stage 1: Get edges in frame
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(gray, 100, 200)

        # Stage 2: Find contours
    #    im2, contours, _ = cv2.findContours(edges, cv2.RETR_TREE,
    #                                    cv2.CHAIN_APPROX_SIMPLE)
        contourresult = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours = contourresult[1]
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        found_glyphs = []
        for contour in contours:
            # Stage 3: Shape check
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01*perimeter, True)

            if len(approx) == QUADRILATERAL_POINTS:
                # Stage 5: Perspective warping
                topdown_quad = get_topdown_quad(gray, approx.reshape(4, 2))
                try:
                    if (topdown_quad.shape[0] < 0 and
                            topdown_quad.shape[1] < 0):
                        print '***** shape invalid!!'

                    # Stage 6: Border check for black pixel @ 5,5
                    resized_shape = resize_image(topdown_quad, SHAPE_RESIZE)
                    if resized_shape[5, 5] > BLACK_THRESHOLD:
                        continue
                    # Stage 7: Glyph pattern
                    glyph_pattern = get_glyph_pattern(resized_shape,
                                                    BLACK_THRESHOLD,
                                                    WHITE_THRESHOLD)
                    glyph_found, glyph_rotation, glyph_substitute = match_glyph_pattern(glyph_pattern)
                except:
                    print 'failed'
                    return None

                if glyph_found:
                    cv2.drawContours(image, [contour], 0, (0, 0, 255), 2)

                    M = cv2.moments(contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    cv2.putText(image, str((cX, cY)),
                                (cX, cY),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                1,
                                (0, 255, 0),
                                2)

                    found_glyphs.append(contour)
                    # # Stage 8: Substitute glyph
                    # substitute_image = cv2.imread('glyphs/images/{}.jpg'.format(glyph_substitute))
                    #
                    # for _ in range(glyph_rotation):
                    #     substitute_image = rotate_image(substitute_image, 90)
                    #
                    # image = add_substitute_quad(image, substitute_image,
                    #                             approx.reshape(4, 2))
        return image
