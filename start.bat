@echo off
chcp 65001 >nul

:: Проверка прав (как в варианте 2) — опустим для краткости, но можно добавить
cd /d "%~dp0"
call .venv\Scripts\activate.bat

if "%~1"=="" (
    echo Перетащите аудиофайл на этот скрипт или укажите путь:
    set /p "audiofile=Путь к файлу: "
) else (
    set "audiofile=%~1"
)

python main.py "%audiofile%"
pause