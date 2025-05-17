@echo off
echo === Updating pip ===
"C:\Python311\python.exe" -m pip install --upgrade pip

echo === Installing dependencies ===
"C:\Python311\python.exe" -m pip install -r requirements.txt

echo === Running the Flask app ===
"C:\Python311\python.exe" app.py
