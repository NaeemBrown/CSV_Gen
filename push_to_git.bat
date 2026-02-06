@echo off
echo --- Starting the Git Push Process ---

:: Initialize Git if not already done
if not exist .git (
    git init
    echo [✓] Git Initialized
)

:: Add all files (the GUI, the logic, and the Batch file)
git add .

:: Commit with a message
set /p commit_msg="Enter your commit message (e.g., v1.0 GUI Launch): "
git commit -m "%commit_msg%"

echo.
echo --- Next Steps for Naeem ---
echo 1. Go to github.com/new
echo 2. Name your repo 'Digital-Plumber-CT'
echo 3. Copy the URL and run:
echo    git remote add origin YOUR_URL_HERE
echo    git branch -M main
echo    git push -u origin main
echo.
pause