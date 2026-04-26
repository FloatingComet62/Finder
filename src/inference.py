"""
a. Function to run inference on the model
I. Function should contain the proper marked outputs
II. Inference time
III. FPS written on the frame
"""

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import cv2
import subprocess
from logger import ModuleLogger
import time
import threading
import queue

logger = ModuleLogger("Inference")

capture = None
models = []
output = None
output_logs = None
__last_frame_time = time.time()
__last_results = []
__avg_latency = 0
__step_count = 0

frame_queue = queue.Queue(maxsize=1)
result_queues = []


def annotate(frame, results):
    annotator = Annotator(frame)
    for i, result in enumerate(results):
        for box in result.boxes:
            b = box.xyxy[0]
            c = int(box.cls)
            conf = float(box.conf)
            label = f"{models[i].names[c]} {conf:.2f}"
            annotator.box_label(b, label)

    return annotator.result()


def inference_worker(i):
    model = models[i]
    result_queue = result_queues[i]

    def inner():
        while True:
            frame = frame_queue.get()
            if frame is None:
                break

            results = model(frame, verbose=False)

            if result_queue.full():
                try:
                    result_queue.get_nowait()
                except queue.Empty:
                    pass
            result_queue.put([results[0]])

    return inner


def init(model_paths, video_capture=0, output_log_file_path="output.log"):
    logger.debug(
        f"Initialization. Model = {model_paths}, VideoCapture = {video_capture}, OutputLogs = {output_log_file_path}"
    )
    global capture, output, output_logs
    capture = cv2.VideoCapture(video_capture)

    for i, model_path in enumerate(model_paths):
        models.append(YOLO(model_path))
        result_queues.append(queue.Queue(maxsize=1))
        __last_results.append(None)

        worker = threading.Thread(target=inference_worker(i), daemon=True)
        worker.start()

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
    global __last_frame_time, __step_count, __avg_latency
    new_time = time.time()
    latency = round((new_time - __last_frame_time) * 1000, 2)
    __last_frame_time = new_time

    __avg_latency = round(
        (__avg_latency * __step_count + latency) / (__step_count + 1), 2
    )
    __step_count += 1
    logger.debug(f"Step (Latency: {latency}ms) (Average: {__avg_latency}ms)")

    ret, frame = capture.read()
    if not ret:
        return (False, [])

    if frame_queue.full():
        try:
            frame_queue.get_nowait()
        except queue.Empty:
            pass
    frame_queue.put(frame)

    all_results = []

    for i, result_queue in enumerate(result_queues):
        try:
            result = result_queue.get_nowait()
            __last_results[i] = result
            all_results.append(result)
            frame = annotate(frame, result)
        except queue.Empty:
            if __last_results[i] is not None:
                frame = annotate(frame, __last_results[i])
            else:
                pass

    try:
        output.stdin.write(frame.tobytes())
    except BrokenPipeError:
        return (False, [])

    return (True, all_results)


def deinit():
    logger.debug("Deinitialization")
    capture.release()
    output.stdin.close()
    output_logs.close()
