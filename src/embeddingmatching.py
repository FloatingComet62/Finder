import os
import pickle
import numpy as np
import face_recognition
from logger import ModuleLogger

logger = ModuleLogger("Embedding Matcher")


class EmbeddingMatcher:
    def __init__(self, save_folder):
        os.makedirs(save_folder, exist_ok=True)
        self.save_folder = save_folder
        self.files = set(os.listdir(save_folder))

    def save_parents(self, parents):
        for parent in parents:
            if parent.id in self.files:
                continue

            f = open(f"{self.save_folder}/{parent.id}.pkl", "wb")
            pickle.dump(parent, f)
            f.close()
            self.files.add(parent.id)

    def find_resembling_parent(self, comparing_frame):
        rgb_frame = np.ascontiguousarray(
            comparing_frame[:, :, ::-1],
            dtype=np.uint8
        )

        frame_encodings = face_recognition.face_encodings(rgb_frame)

        if len(frame_encodings) == 0:
            logger.warn("No face found in the input frame")
            return 0

        frame_encoding = frame_encodings[0]
        best_match = None
        best_distance = 1.0

        for parent_filename in self.files:
            f = open(f"{self.save_folder}/{parent_filename}", "rb")
            parent = pickle.load(f)
            f.close()

            rgb_parent = np.ascontiguousarray(
                parent.frame[:, :, ::-1],
                dtype=np.uint8
            )

            parent_encodings = face_recognition.face_encodings(rgb_parent)

            if len(parent_encodings) == 0:
                continue

            parent_encoding = parent_encodings[0]

            distance = face_recognition.face_distance(
                [parent_encoding],
                frame_encoding
            )[0]

            if distance < best_distance:
                best_distance = distance
                best_match = parent_filename

        if best_distance < 0.6:
            return best_match

        return None
