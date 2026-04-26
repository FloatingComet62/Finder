"""
a. Model training code and it's architecture
"""

# There is no official pretrained version of YOLO for SKU-110K
from ultralytics import YOLO

# import time

# i tried yolov26n, but it neeeds 16GBs of VRAM, and i ain't got that
model = YOLO("yolov8s.pt")

results = model.train(
    data="SKU-110K.yaml",
    epochs=1,
    imgsz=640,
    fraction=0.1,
    # project="runs/sku110k",
    # name=time.time(),
    # exist_ok=False,
)

model.save("yolo8s-sku110k.pt")
