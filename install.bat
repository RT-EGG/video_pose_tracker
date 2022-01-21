@setlocal
@pushd %~dp0

py -3.10 -m venv venv

call %~dp0venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
call deactivate

@popd
@endlocal

exit /b 0
