# main.py
from flask import Flask, Response, request
from camera import VideoCamera
import socket
import sys
import argparse as ap
import cvhelpers
from barcode import find_barcode
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
        image = camera.get_frame()
        frame = cvhelpers.encode_to_jpeg(image)
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen_frames(camera, transform):
    print 'Starting the stream'
    camera.start_frame_grab(ROTATION, ZOOM, CROP)
    while True:
        image = camera.get_frame()
        if transform is not 'stream' and routes[transform]:
            image = routes[transform](image)
        frame = cvhelpers.encode_to_jpeg(image)
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen_barcode(camera):
    print 'Starting barcode stream'
    camera.start_frame_grab(ROTATION, ZOOM, CROP)
    while True:
        image = find_barcode(camera.get_frame())
        frame = cvhelpers.encode_to_jpeg(image)
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen_glpyh(camera):
    print 'Starting glyph'
    camera.start_frame_grab(ROTATION, ZOOM, CROP)
    while True:
        image = gd.find_glyph(camera.get_frame())
        frame = cvhelpers.encode_to_jpeg(image)
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def add_camera(cam_name):
    if(cam_name not in cameras):
        print 'Camera doesn\'t exist, adding new camera ', cam_name
        cam = VideoCamera(int(cam_name))
        if(cam.is_open() is False):
            return None, 'Camera %s failed to open' % cam_name
        cameras[cam_name] = cam
        return cameras[cam_name], 'Opened camera'
    return cameras[cam_name], 'Cameras already opened'


# old routes - to be removed
#
# @app.route('/barcode/<cam_name>')
# def stream_barcode(cam_name):
#     try:
#         (success, message) = add_camera(cam_name)
#         if(success is False):
#             return message
#         return Response(gen_barcode(cameras[cam_name]),
#                         mimetype='multipart/x-mixed-replace; boundary=frame')
#     except:
#         print 'Failed to retreive bar stream from camera ', sys.exc_info()[0]
#
#         return 'Failed to retreive barcode stream from camera ', cam_name
#
#
# @app.route('/glyph/<cam_name>')
# def stream_glyph(cam_name):
#     try:
#         (success, message) = add_camera(cam_name)
#         if(success is False):
#             return message
#         return Response(gen_glpyh(cameras[cam_name]),
#                         mimetype='multipart/x-mixed-replace; boundary=frame')
#     except:
#         print 'Failed to retreive bar stream from camera ', sys.exc_info()[0]
#
#         return 'Failed to retreive barcode stream from camera ', cam_name
#
#
# @app.route('/stream/<cam_name>')
# def stream_camera(cam_name):
#     try:
#         cam_num = int(cam_name)
#         (success, message) = add_camera(cam_num)
#         if(success is False):
#             return message
#         return Response(gen(cameras[int(cam_num)]),
#                         mimetype='multipart/x-mixed-replace; boundary=frame')
#     except:
#         print 'Failed to retreive c stream from camera. Excpetion: ', \
#                 sys.exc_info()[0]
#         return 'Failed to retreive c stream from camera ', cam_num


@app.route('/stream/<int:cam_num>')
def start_stream(cam_num):
    try:
        (camera, message) = add_camera(cam_num)
        if(camera is None):
            print 'none camera in stream'
            return message
        transform = request.args.get('transform') or 'stream'
        return Response(gen(camera, transform),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except:
        print 'Failed to retreive stream from camera. ', sys.exc_info()[0]
        return 'Failed to retreive stream from camera ', cam_num


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/end')
def stop_program():
    print cameras
    for num, cam in cameras.iteritems():
        cam.stop_frame_grab()
    shutdown_server()
    return 'Stopped all cameras.'


parser = ap.ArgumentParser(description="Start the webcam stream")
parser.add_argument('--local', action='store_true')
parser.add_argument('--rotate', default=0,
                    help='rotation of the image')
parser.add_argument('--zoom', default=1,
                    help='zoom level of the image as a percent')
# To make the input integers
parser.add_argument('--crop', nargs='+', type=int, default=(0, 0),
                    help='Width, Height values to crop. Cropping is \
                    symmetric')

# mapping of routes to the functions that supply images
routes = {
    'stream': None,
    'barcode': find_barcode,
    'glyph': gd.find_glyph
}


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
    print "Starting camera on ", host
    try:
        app.run(host=host, port=port, threaded=True)
    except socket.error:
        print "Camera already running, exiting."
