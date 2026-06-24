from flask import Flask, Response, render_template
import cv2
import threading
from SpinbotStationsDrivers import imagestation, sdc

app = Flask(__name__)


def run_pump():
    while True:
        """Runs the syringe pump sequence. This blocks for as long as the pump runs."""
        print("Starting pump sequence...")
        var = sdc()
        var.test()
        print("Pump sequence complete.")
        text = input("Press r to run again...")  # Keep the thread alive until user input
        if text.lower() == 'r':
            continue
        else:
            break



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
    pump_thread = threading.Thread(target=run_pump, daemon=True)
    pump_thread.start()          # pump starts running in the background...

    app.run(host='0.0.0.0', port=5000, debug=False)   # ...while Flask serves the stream