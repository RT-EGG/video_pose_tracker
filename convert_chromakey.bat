@setlocal
@pushd %~dp0

call %~dp0venv\Scripts\activate

set INPUT=%~1
set OUTPUT=%~dpn1_chromakey%~x1

python scripts\video_pose_tracker.py^
 -i %INPUT%^
 -o %OUTPUT%^
 --mode chromakey^
 --background %~2^
 --chromakey_clip_mode %~3

call deactivate

@popd
@endlocal

@exit /b 0
