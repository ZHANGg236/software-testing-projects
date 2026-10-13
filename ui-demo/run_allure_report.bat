@echo off
chcp 65001 >nul
powershell -ExecutionPolicy Bypass -File "%~dp0run_allure_report.ps1"
