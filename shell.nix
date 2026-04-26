{ pkgs ? import <nixpkgs> {} }:

let
  lib = pkgs.lib;
  py = pkgs.python313;
  # ultralytics = py.pkgs.ultralytics.overridePythonAttrs (old: rec {
  #   version = "8.4.41";
  #
  #   src = pkgs.fetchPypi {
  #     pname = "ultralytics";
  #     inherit version;
  #     sha256 = "sha256-HMw/Xz5+6JC8EEP48OaeWto+gCEVda6W+06kK6HRjcg=";
  #   };
  # });
  # ultralytics = py.pkgs.buildPythonPackage rec {
  #   pname = "ultralytics";
  #   version = "8.4.41";
  #   format = "pyproject";
  #
  #   src = pkgs.fetchPypi {
  #     inherit pname version;
  #     sha256 = "sha256-HMw/Xz5+6JC8EEP48OaeWto+gCEVda6W+06kK6HRjcg=";
  #   };
  #
  #   build-system = [ py.pkgs.setuptools ];
  #
  #   propagatedBuildInputs = with py.pkgs; [
  #     torchWithCuda
  #     torchvision
  #     opencv4
  #     numpy
  #     pillow
  #     pyyaml
  #     requests
  #     scipy
  #     tqdm
  #     psutil
  #     py-cpuinfo
  #     matplotlib
  #     pandas
  #     ultralytics-thop
  #   ];
  #
  #   postInstall = ''
  #     # ultralytics expects 'opencv-python' but we provide opencv4
  #     echo "opencv-python" >> $out/lib/python*/site-packages/ultralytics-${version}.dist-info/METADATA
  #   '';
  #
  #   pythonRemoveDeps = [ "opencv-python" "polars" ];
  #   doCheck = false;
  # };
  pythonEnv = py.withPackages (ps: with ps; [
    pip
    opencv4
    numpy
    # torch
    # torchvision
    tensorboard
    python-dotenv
    ultralytics
    polars
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
    pythonEnv
    wget
    v4l-utils
    ffmpeg
    # cudaPackages.cudatoolkit
    # cudaPackages.cudnn
    # linuxPackages.nvidia_x11
    # export CUDA_PATH=${pkgs.cudaPackages.cudatoolkit}
    # export LD_LIBRARY_PATH=/run/opengl-driver/lib
    # :/run/opengl-driver-32/lib:${pkgs.cudaPackages.cudatoolkit}/lib:${pkgs.cudaPackages.cudnn}/lib:$LD_LIBRARY_PATH
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
