{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    pip
    opencv4
    numpy
    ultralytics
    python-dotenv
  ]);
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    pythonEnv
    v4l-utils
    ffmpeg
  ];

  shellHook = ''
    export OPENCV_VIDEOIO_PRIORITY_V4L2=1
    echo "OpenCV ready (headless)"
    echo "Camera: $(ls /dev/video* 2>/dev/null || echo 'none found')"
  '';
}
