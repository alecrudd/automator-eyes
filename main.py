# main.py
from flask import Flask, Response
from camera import VideoCamera
import socket

app = Flask(__name__)


port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

cameras = {}


@app.route('/')
def index():
    return "automatorpi test"


def gen(camera):
    camera.start_frame_grab()
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen_barcode(camera):
    print 'starting barcode feed'
    camera.start_frame_grab()
    while True:
        frame = camera.get_barcode_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/barcode/<camnum>')
def stream_barcode(camnum):
    try:
        if(camnum not in cameras):
            cameras[camnum] = VideoCamera(camnum)
            if(cameras[camnum].isOpen is False):
                return 'Camera %d failed to open' % camnum
        return Response(gen_barcode(cameras[int(camnum)]),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except:
        return 'Failed to retreive barcode stream from camera ' + camnum


@app.route('/stream/<camnum>')
def stream_camera(camnum):
    try:
        if(camnum not in cameras):
            cameras[camnum] = VideoCamera(camnum)
            if(cameras[camnum].isOpen is False):
                return 'Camera %d failed to open' % camnum
        return Response(gen(cameras[int(camnum)]),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except:
        return 'Failed to retreive c stream from camera ' + camnum


if __name__ == '__main__':
    app.run(host=ip, port=port, threaded=True)
