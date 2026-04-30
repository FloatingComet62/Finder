import cv2
from ultralytics import YOLO
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

FACE_DETECTION_MODEL = os.environ["FACE_DETECTION_MODEL"]
FACE_DETECTION_CLASS = os.environ["FACE_DETECTION_CLASS"]

print(FACE_DETECTION_MODEL, FACE_DETECTION_CLASS)

model = YOLO(FACE_DETECTION_MODEL)
model(np.zeros((640, 384, 3)))


def main():
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()

    if not ret:
        capture.release()
        return
    capture.release()

    print(1)
    results = model(frame)
    print(results)


if __name__ == "__main__":
    main()
