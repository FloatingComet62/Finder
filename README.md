# Finder
Using YOLO on Jetson Nano for Item Tracking and Lost and Found Service

## Project Abstract

### Problem Statement
Security cameras cannot automatically determine ownership of items left in view. When items are lost or abandoned, there is no efficient way to identify their rightful owner or determine when an item has been left unattended.

### Role of Edge Computing
- **Components that run on Jetson Nano**: YOLO inference pipelines (yolov8s-oiv7.pt for faces/people, epoch12.pt for retail items), real-time object tracking via ItemTagger, face embedding extraction using EmbeddingMatcher
- **Justification for using edge computing instead of cloud-only solutions**: Processing video streams in the cloud raises privacy concerns and introduces unacceptable latency for real-time tracking
- **Benefits such as reduced latency, offline capability, or efficiency**: Millisecond-level inference latency, operates without network connectivity, all data remains on-premises for privacy

### Project Models

### Methodology
1. **Input**: Video stream captured via webcam (cv2.VideoCapture)
2. **Preprocessing**: YOLO models run in parallel threads, ItemTagger extracts positions, color histograms, and velocity vectors to track objects across frames
3. **Processing**: ItemOwnershipProcessor classifies detections as parents (persons) or items, calculates proximity-based ownership confidence
4. **Abandonment Detection**: When distance between item and associated person exceeds threshold (100px), ownership confidence decreases; items with low confidence are saved as abandoned
5. **Output**: Annotated real-time video via ffplay, abandoned item images to tagged_objects/, ownership relationships serialized to abandoned_objects

### Model Details
- **Type of model used and its architecture**: YOLOv8s architecture with custom training on SKU-110K dataset
- **Input size and format**: 640x640 RGB images
- **Framework used (PyTorch, TensorFlow, etc.)**: PyTorch (Ultralytics library)
- **Any optimization techniques**: Threaded inference with dedicated worker threads per model, frame queuing system, CUDA acceleration on Jetson Nano

## Project Output
- Real-time annotated video output via ffplay pipe displaying bounding boxes and labels
- Saved abandoned item images in tagged_objects/ directory
- Face embeddings and person images stored in parent_objects/ for matching
- Ownership relationship data in abandoned_objects pickle file
- Lost & Found Service: Users submit their photo via input_lostandfound.py, face is matched against saved embeddings (threshold 0.6), system returns their previously tracked items
- **Performance Metrics**: Per-step latency tracking (ms), running average latency, FPS estimation via threaded inference architecture
- **Performance Comparison**: Jetson Nano with CUDA acceleration provides real-time inference suitable for edge deployment; cloud-only alternatives introduce latency unsuitable for real-time tracking

## Setup Instructions

### Nix
```bash
nix-shell
just dev
```

### Non-Nix
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```
