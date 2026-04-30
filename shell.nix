{ pkgs ? import <nixpkgs> {} }:

let
  lib = pkgs.lib;
  py = pkgs.python313;
  pythonEnv = py.withPackages (ps: with ps; [
    pip
    opencv4
    numpy
    tensorboard
    python-dotenv
    ultralytics
    polars
    face-recognition
  ]);
  models = {
    yolov8s = {
      url = "https://huggingface.co/Ultralytics/YOLOv8/resolve/main/yolov8s.pt";
      sha256 = "sha256-Jo5btUxkDJbDUQIkgzvC7qyrQTXG3rQVAhVuOZhrVi0=";
    };
    yolov26s = {
      url = "https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26s.pt";
      sha256 = "sha256-ZG+Lw/4KZWgD2VwpT3hSMhdIyynRNGahr4hi4ts4Shs=";
    };
    yolov8s-oiv7 = {
      url = "https://github.com/ultralytics/assets/releases/download/v8.4.0/yolov8s-oiv7.pt";
      sha256 = "sha256-RmMIbhuO28QgKp7FibAxle0Unviqi+60tQPg41/xcxo=";
    };
  };

  fetchedModels = lib.mapAttrs (_: v:
    pkgs.fetchurl {
      inherit (v) url sha256;
    }
  ) models;
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    just
    pythonEnv
    wget
    v4l-utils
    ffmpeg
  ];

  shellHook = ''
    export LD_PRELOAD=/run/opengl-driver/lib/libcuda.so.1
    export LD_LIBRARY_PATH=/run/opengl-driver/lib:/run/opengl-driver-32/lib:$LD_LIBRARY_PATH
    echo "OpenCV $(python -c 'import cv2; print(cv2.__version__)') ready"
    echo "CUDA: $(python -c 'import torch; print(torch.cuda.is_available())')"
    echo "Camera: $(ls /dev/video* 2>/dev/null || echo 'none found')"

    ${lib.concatStringsSep "\n" (
      lib.mapAttrsToList (name: path: ''
        ln -sf ${path} "${name}.pt"
        echo "Linked ${name}.pt"
      '') fetchedModels
    )}
  '';
}
