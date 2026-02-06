@echo off
chcp 65001 >nul
cls

echo 2026智海宝安区设计大赛 - 唐荣麒作品
echo 启动器 (无毒版本)
echo ==============================
echo.

:: 直接安装pgzero（不检查）
pip install pgzero --quiet >nul 2>&1

echo 启动主程序...
python main.py

:: 如果失败则暂停
if errorlevel 1 pause