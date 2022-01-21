@setlocal
@pushd %~dp0

call %~dp0venv\Scripts\activate

set INPUT=%~1
set OUTPUT=%~dpn1_pose%~x1

python scripts\video_pose_tracker.py^
 -i %INPUT%^
 -o %OUTPUT%^
 --mode pose

call deactivate

@popd
@endlocal

@exit /b 0
