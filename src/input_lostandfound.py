from ultralytics import YOLO
from dotenv import load_dotenv
import os
import numpy as np
import embeddingmatching
import pickle

load_dotenv()

FACE_DETECTION_MODEL = os.environ["FACE_DETECTION_MODEL"]
FACE_DETECTION_CLASS = os.environ["FACE_DETECTION_CLASS"]

model = YOLO(FACE_DETECTION_MODEL)
assert FACE_DETECTION_CLASS in model.names.values()
model(np.zeros((640, 384, 3)), device="cpu")

matcher = embeddingmatching.EmbeddingMatcher("parent_objects")


def main():
    import cv2
    capture = cv2.VideoCapture(0)

    result = None
    result_got = False
    while True:
        ret, frame = capture.read()

        if not ret:
            break

        for box in model(frame)[0].boxes:
            if model.names[int(box.cls)] != FACE_DETECTION_CLASS:
                continue
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cutted_frame = frame[y1:y2, x1:x2]
            result = matcher.find_resembling_parent(cutted_frame)
            if result == 0:
                # no face embeddings found, try again
                break
            result_got = True
            break

        if result_got:
            break
    capture.release()

    if result is None:
        print("No face matches found")
        return 1

    with open("abandoned_objects", "rb") as f:
        ownership_table = pickle.load(f)

    result = result[:-4]
    items_owned_by_match = None
    for key, value in ownership_table.items():
        if key.id == result:
            items_owned_by_match = value
            break

    if items_owned_by_match is None:
        print("No items found connected to the face")
        return 1

    print(len(items_owned_by_match), "items found")
    for item in items_owned_by_match.keys():
        print(item)


if __name__ == "__main__":
    exit(main() or 0)
