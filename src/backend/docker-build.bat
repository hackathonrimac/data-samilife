@echo off
REM Script para construir la imagen Docker de la Healthcare API (Windows)

echo ======================================
echo Building Healthcare API Docker Image
echo ======================================
echo.

docker build -t healthcare-api:latest .

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Image built successfully!
    echo.
    echo To run the container:
    echo   docker run -p 8000:8000 --env-file .env healthcare-api:latest
    echo.
    echo Or use docker-compose:
    echo   docker-compose up
) else (
    echo.
    echo ❌ Build failed!
    exit /b 1
)
