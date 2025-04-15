@echo off
set NAME=GCJ25
set START_DATE=2020-01-01
set END_DATE=2024-12-31

echo Running Barchart download for:
echo Symbol: %NAME%
echo Start Date: %START_DATE%
echo End Date: %END_DATE%
echo.

C:\Users\cdsjt\anaconda3\python.exe C:\Users\cdsjt\dev\barchart\selenium_dump.py --name %NAME% --start-date %START_DATE% --end-date %END_DATE%
pause 