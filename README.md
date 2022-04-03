# video_pose_tracker

## Overview
This program convert the video file to
- tracked pose only video
- overlay original video and tracked pose
- chroma key compositing for human clipping

Use [MediaPipe](https://github.com/google/mediapipe) to track pose.  
Supports only single human detection.

Samples in "videos" directory.

## Requirement
Python 3.10 (develop by 3.10.2)

## Getting started
### Windows
1. Install python (required version written in [Requirement](#requirement))
1. Run install.bat.
1. Run bat with argument as input video filepath.

- convert_to_pose.bat
    - Export movie that detected pose on black back-ground.
    - arguments:
    1. input video filepath

- convert_to_overlay.bat  
    - Export movie that overlay detected pose on original movie.
    - arguments:
    1. input video filepath 

- convert_chromakey.bat
    - Export movie that chromakey compositing with any background image.
    - arguments:
    1. input video filepath
    2. background image filepath (must be same dimensions of shape with video.)
    3. clipmode (foreground or background), that means which you want to clip foreground or background.


## TODO
- [ ] Interactive GUI convert tool.
- [ ] Release exe.
