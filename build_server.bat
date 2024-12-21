@echo off
REM Переход в директорию со скриптами
cd ./messenger/scripts/

REM Активация виртуального окружения
call activate.bat

REM Переход обратно в корневую директорию проекта
cd ../..

REM Запуск PyInstaller для сборки server.py в один исполняемый файл
pyinstaller --onefile server.py

REM Пауза, чтобы окно не закрылось сразу после завершения
pause
