"""
a. Function to run inference on the model
I. Function should contain the proper marked outputs
II. Inference time
III. FPS written on the frame
"""

from ultralytics import YOLO
import cv2
import subprocess
import logger
import time

capture = None
model = None
output = None
output_logs = None
__last_frame_time = time.time()


def init(model_path, video_capture=0, output_log_file_path="output.log"):
    logger.debug(
        f"[Inference] Initialization. Model = {model_path}, VideoCapture = {video_capture}, OutputLogs = {output_log_file_path}"
    )
    global capture, model, output, output_logs
    capture = cv2.VideoCapture(video_capture)
    model = YOLO(model_path)

    w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_logs = open(output_log_file_path, mode="w")

    output = subprocess.Popen(
        [
            "ffplay",
            "-f",
            "rawvideo",
            "-pixel_format",
            "bgr24",
            "-video_size",
            f"{w}x{h}",
            "-i",
            "pipe:0",
        ],
        stdin=subprocess.PIPE,
        stdout=output_logs,
        stderr=output_logs,
    )


def step() -> bool:
    global __last_frame_time
    new_time = time.time()
    logger.debug(f"[Inference] Step (Latency: {new_time - __last_frame_time}ms)")
    __last_frame_time = new_time
    ret, frame = capture.read()
    if not ret:
        return False
    results = model(frame)
    annotated = results[0].plot()

    try:
        output.stdin.write(annotated.tobytes())
    except BrokenPipeError:
        return False


def deinit():
    capture.release()
    output.stdin.close()
    output_logs.close()
