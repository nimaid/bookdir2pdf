@echo off

REM DO NOT USE THIS SCRIPT. It is for creating new releases.

set RELEASEDIRNAME="__release__"

set ORIGDIR="%CD%"
set SCRIPTDIR="%~dp0"

cd %SCRIPTDIR%

set BUILDDIR="%SCRIPTDIR%\build"
set DISTDIR="%SCRIPTDIR%\dist"
set RELEASEDIR="%SCRIPTDIR%\%RELEASEDIRNAME%"

del /f /s /q "%BUILDDIR%" 1>nul 2>&1
rmdir /s /q "%BUILDDIR%" 1>nul 2>&1

del /f /s /q "%DISTDIR%" 1>nul 2>&1
rmdir /s /q "%DISTDIR%" 1>nul 2>&1

del /f /s /q "%RELEASEDIR%" 1>nul 2>&1
rmdir /s /q "%RELEASEDIR%" 1>nul 2>&1

echo Building portable EXE...
call conda run -n nested-pdf-merge_build pyinstaller ^
    --noconfirm ^
    --onefile ^
    --icon=icon.ico ^
    nested-pdf-merge.py
if errorlevel 1 goto ERROR

del /f /s /q "%BUILDDIR%" 1>nul 2>&1
rmdir /s /q "%BUILDDIR%" 1>nul 2>&1

rename "%DISTDIR%" "%RELEASEDIRNAME%" 1>nul 2>&1
if errorlevel 1 goto ERROR

goto DONE


:ERROR
cd %ORIGDIR%
echo Portable EXE build failed!
exit /B 1

:DONE
cd %ORIGDIR%
echo Portable EXE build done!
exit /B 0