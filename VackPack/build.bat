@echo off
echo 🚀 Building VacPack .exe...

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Clean previous builds
rmdir /s /q build
rmdir /s /q dist
del /q *.spec

REM Use full path to pyinstaller
.venv\Scripts\pyinstaller.exe main.py --name VacPack --onefile --windowed --icon=vacpack.ico

echo ✅ Done! Your .exe is in the dist folder.
pause
