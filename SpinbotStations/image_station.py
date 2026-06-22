import cv2, os
from datetime import datetime

class ImageStation:
    def __init__(self, camera_index=0, capture_dir=None):
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
        
        self.capture_dir = capture_dir if capture_dir else os.path.join(os.getcwd(), "captures")
        if not os.path.exists(self.capture_dir):
            os.makedirs(self.capture_dir)

    def wait_for_image_request(self):
        pass

    def move_stage_into_position(self):
        pass

    def capture_image(self):
        if not self.cap.isOpened():
            print("Cannot open camera")
            return
        ret, frame = self.cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.jpg"
        filepath = os.path.join(self.capture_dir, filename)
        cv2.imwrite(filepath, frame)
        print(f"Image captured and saved as {filename}")

    def move_stage_back(self):
        pass

    def send_image_to_spinbot(self):
        pass

    def process_image_request(self):
        self.wait_for_image_request()
        self.move_stage_into_position()
        self.capture_image()
        self.move_stage_back()
        self.send_image_to_spinbot()