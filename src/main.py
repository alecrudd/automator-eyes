# main.py
from flask import Flask, render_template, Response
from camera import VideoCamera
from barcode import find_barcode

app = Flask(__name__)


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


@app.route('/get_barcode')
def get_combined():
    return Response(gen_barcode(VideoCamera(0)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_left')
def right_video_feed():
    return Response(gen(VideoCamera(0)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_right')
def left_video_feed():
    return Response(gen(VideoCamera(1)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
