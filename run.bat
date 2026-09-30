@echo off
echo ========================================================
echo   Starting Smart Search Online Store...
echo   ADSA (AVL Tree) + DMGT (Set Theory) + Python Recommender
echo ========================================================
echo.

IF NOT EXIST "products.csv" (
    echo [Setup] Generating 5,000+ realistic electronics products...
    python generate_data.py
)

echo [Server] Launching application on http://127.0.0.1:5000 ...
python app.py
pause
