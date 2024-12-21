@echo off
REM Переход в директорию со скриптами
cd ./messenger/scripts/

REM Активация виртуального окружения
call activate.bat

REM Переход обратно в корневую директорию проекта
cd ../..

REM Запуск PyInstaller для сборки client.py в один исполняемый файл
pyinstaller --onefile client.py

REM Пауза, чтобы окно не закрылось сразу после завершения
pause
