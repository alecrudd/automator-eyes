# main.py
from flask import Flask, render_template, Response
from camera import VideoCamera
import socket

app = Flask(__name__)


port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen_barcode(camera):
    while True:
        frame = camera.get_barcode()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/barcode/<variable>')
def get_barcode(variable):
    return Response(gen_barcode(VideoCamera(int(variable))),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream/<variable>')
def stream_camera(variable):
    print 'using camera: ' + variable
    return Response(gen(VideoCamera(int(variable))),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host=ip, port=port, threaded=True)
