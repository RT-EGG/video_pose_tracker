# video_pose_tracker

## Overview
This program convert the video file to
- tracked pose only video
- overlay original video and tracked pose

Use [MediaPipe](https://github.com/google/mediapipe) to track pose.  
Supports only single human detection.

Samples in "videos" directory.

## Requirement
Python 3.10 (develop by 3.10.2)

## Getting started
### Windows
1. Run install.bat.
1. Run bat with argument as input video filepath.

- convert_to_pose.bat
    - Export movie that detected pose on black back-ground.

- convert_to_overlay.bat  
    - Export movie that overlay detected pose on original movie.


## TODO
- [ ] Interactive GUI convert tool.
