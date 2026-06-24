import cv2
import os
import flask
import threading
from datetime import datetime

class imagestation:
    def __init__(self, camera_index=0, capture_dir=None):
        self.cap = cv2.VideoCapture(camera_index)
        self.check_camera()

        self.capture_dir = capture_dir if capture_dir else os.path.join(os.getcwd(), "captures")
        if not os.path.exists(self.capture_dir):
            os.makedirs(self.capture_dir)

    def check_camera(self) -> bool:
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Can't receive frame")
        return True

    def capture_image(self):
        self.check_camera()
        ret, frame = self.cap.read()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.jpg"
        filepath = os.path.join(self.capture_dir, filename)
        cv2.imwrite(filepath, frame)
        print(f"Image captured and saved as {filename}")

    def start_stream(self):
        #TODO Need to finish this section
        pass

    def generate_frames(self):
        cam = cv2.VideoCapture(0)
        if not self.check_camera():
            return
        
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
