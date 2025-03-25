@echo off
echo Creating Python virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Setup completed successfully!

echo.
echo Virtual environment is now active. You can run:
echo     python main.py

cmd /k
