import cv2
import os
from datetime import datetime


def capture_image():
    # Captures an image and places it in the captures directory with a timestamped filename
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"capture_{timestamp}.jpg"
    cv2.imwrite(os.path.join(capture_dir, filename), frame)
    print(f"Image captured and saved as {filename}")
    cap.release()

capture_dir = os.path.join(os.path.dirname(__file__), 'captures')
print(capture_dir)

if __name__ == "__main__":
    if not os.path.exists(capture_dir):
        # if the captured directory does not exist, create it
        os.makedirs(capture_dir)
    while True:
        if input("Press Enter to capture an image (or type 'q' to quit): ").lower() == 'q':
            break
        capture_image()