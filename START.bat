@echo off
chcp 65001 >nul
echo ==========================================
echo   ROTEIRISTA AI - Iniciando Servidor
echo ==========================================
echo.

:: Abre porta no firewall (precisa rodar como admin)
netsh advfirewall firewall add rule name="Roteirista AI" dir=in action=allow protocol=tcp localport=5001 >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Porta 5001 liberada no firewall
) else (
    echo [AVISO] Nao foi possivel liberar firewall. Execute como Administrador.
)

echo.
echo [OK] Servidor iniciando...
echo [INFO] Acesse no navegador: http://127.0.0.1:5001
echo [INFO] Na mesma WiFi: http://192.168.3.51:5001
echo.
echo Pressione CTRL+C para parar o servidor
echo ==========================================

python web_app.py

pause
