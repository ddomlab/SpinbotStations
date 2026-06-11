from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)


def generate_frames():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        raise RuntimeError("Could not open camera")

    try:
        while True:
            success, frame = cam.read()
            if not success:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'
                + frame_bytes +
                b'\r\n'
            )
    finally:
        cam.release()


@app.route('/stream')
def stream():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
