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

cameras = []


def find_cameras():
    # create a new camera, add it to the list
    print 'Finding camera 0'
    cameras.append(VideoCamera(0))


@app.route('/')
def index():
    return "automatorpi"


def gen(camera):
    camera.start_frame_grab()
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen_barcode(camera):
    print 'starting barcode feed'
    camera.start_frame_grab()
    while True:
        frame = camera.get_barcode()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/barcode/<camnum>')
def get_barcode(camnum):
        return Response(gen_barcode(cameras[int(camnum)]),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream/<camnum>')
def stream_camera(camnum):
        try:
            return Response(gen(cameras[int(camnum)]),
                            mimetype=
                            'multipart/x-mixed-replace; boundary=frame')
        except:
            return 'Failed to retreive stream from camera ' + camnum


if __name__ == '__main__':
    find_cameras()
    app.run(host=ip, port=port, threaded=True)
