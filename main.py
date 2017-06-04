# main.py
from flask import Flask, Response
from camera import VideoCamera
import socket
import sys
import argparse as ap
import glyphdetector as gd


app = Flask(__name__)


port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
host = s.getsockname()[0]
s.close()

cameras = {}


@app.route('/')
def index():
    return "automatorpi test"


def gen(camera):
    print 'Starting the normal stream'
    camera.start_frame_grab(ROTATION, ZOOM, CROP)
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen_barcode(camera):
    print 'Starting barcode stream'
    camera.start_frame_grab(ROTATION, ZOOM, CROP)
    while True:
        frame = camera.get_barcode_frame()
        if frame is None:
            print 'no barcode frame'
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen_glpyh(camera):
    print 'Starting glyph'
    camera.start_frame_grab(ROTATION, ZOOM, CROP)
    while True:
        frame = camera.get_glyph_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def add_camera(cam_name):
    if(cam_name not in cameras):
        print 'Camera doesn\'t exist, adding new camera ', cam_name
        cam = VideoCamera(int(cam_name))
        if(cam.is_open() is False):
            return False, 'Camera %s failed to open' % cam_name
        cameras[cam_name] = cam
        return True, 'Opened camera'
    return True, 'Cameras already opened'


@app.route('/barcode/<cam_name>')
def stream_barcode(cam_name):
    try:
        (success, message) = add_camera(cam_name)
        if(success is False):
            return message
        return Response(gen_barcode(cameras[cam_name]),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except:
        print 'Failed to retreive bar stream from camera ', sys.exc_info()[0]

        return 'Failed to retreive barcode stream from camera ', cam_name


@app.route('/glyph/<cam_name>')
def stream_glyph(cam_name):
    try:
        (success, message) = add_camera(cam_name)
        if(success is False):
            return message
        return Response(gen_glpyh(cameras[cam_name]),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except:
        print 'Failed to retreive bar stream from camera ', sys.exc_info()[0]

        return 'Failed to retreive barcode stream from camera ', cam_name


@app.route('/stream/<cam_name>')
def stream_camera(cam_name):
    try:
        # cam_num = int(cam_name)
        (success, message) = add_camera(cam_name)
        if(success is False):
            return message
        return Response(gen(cameras[cam_name]),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except:
        print 'Failed to retreive c stream from camera. Excpetion: ', \
                sys.exc_info()[0]
        return 'Failed to retreive c stream from camera ', cam_name


parser = ap.ArgumentParser(description="Start the webcam stream")
parser.add_argument('--local', action='store_true')
parser.add_argument('--rotate', default=0,
                    help='rotation of the image')
parser.add_argument('--zoom', default=1,
                    help='zoom level of the image as a percent')
# To make the input integers
parser.add_argument('--crop', nargs='+', type=int, default=(0,0),
                    help='Width, Height values to crop. Cropping is \
                    symmetric')


args = parser.parse_args()
try:
    ROTATION = float(args.rotate)
    ZOOM = float(args.zoom)
    CROP = args.crop
except ValueError:
    print "Invalid rotate/zoom setting specified!!"

if __name__ == '__main__':
    if args.local:
        host = 'localhost'
    print host
    app.run(host=host, port=port, threaded=True)
