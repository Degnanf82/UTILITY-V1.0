??&cls
@setlocal DisableDelayedExpansion
@echo off & pushd "%CD%" & CD /D "%~dp0"
TITLE TOOL UTILITY BY DEGNANF V1.0
MODE con:cols=85 lines=35
chcp 65001
color 02
set current_dir=%cd%


:inicio
cls
call :c 05 "                                   BIENVENID@: %USERNAME%  "
echo.
echo.
echo  █████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗
echo  ╚════╝╚════╝╚════╝╚════╝╚═══
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[1: Visual C all-in-one]░░░░░░░░░░░░[8: WEB FRP/TOOLS]░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[2: ENABLE UNSIGNED DRIVERS]░░░░░░░░[9: FIRMWARE SAMSUNG (DIRECT)]░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[3: ACTIVADOR IDM]░░░░░░░░░░░░░░░░░░[10: CONTACTO]░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[4: ACTIVADOR MICROSOFT]░░░░░░░░░░░░[11: OTA UPDATES SAMS/OPPO/MI (ADB)]░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[5: WINDOWS DEFENDER REMOVE]░░░░░░░░[12: ENABLE ADB SAMSUNG (MTP)(old)]░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[6: DRIVERS FOR ANDROID (ALL)]░░░░░░[13: ACTIVAR PUERTO DIAG (MI)(ROOT)]░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[7: SCREEN MIRROR ANDROID(ADB)]░░░░░[14: ]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ╚═╝░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░╚═╝
echo  █████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗
echo  ╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝
echo   ║
SET /p var= ^> ╚════════════════════════►  SELECCIONE UNA OPCION [ESCRIBE EL NUMERO]: 

if "%var%"=="1" goto op1
if "%var%"=="2" goto op2
if "%var%"=="3" goto op3
if "%var%"=="4" goto op4
if "%var%"=="5" goto menu
if "%var%"=="6" goto op6
if "%var%"=="7" goto op7
if "%var%"=="8" goto op8
if "%var%"=="9" goto op9
if "%var%"=="10" goto op10
if "%var%"=="11" goto op11
if "%var%"=="12" goto op12
if "%var%"=="13" goto op13
if "%var%"=="14" goto op14

echo. El numero "%var%" no es una opcion valida, por favor intente de nuevo.
echo.
pause
echo.
goto:inicio

:op1
echo.
echo.
call :c 0E " ══════════► DIRIGIENDO A LA DESCARGA:     "
start https://www.mediafire.com/file/nwy3evzmbaavbz4/Visual-C-Runtimes-All-in-One-May-2023.rar/file
call :c D2 "LISTO"
echo.
echo.
call :c 04 "[PRECIONE CUALQUIER TECLA PARA REGRESAR]"
pause >null
goto:inicio


:op2
echo.
	call :c 0E " ══════════► PROCESO : "
	call :c 5 "DESACTIVANDO USO OBLIGATORIO DE CONTROLADORES FIRMADOS"
	echo.
	bcdedit.exe -set loadoptions DDISABLE_INTEGRITY_CHECKS >nul 2>&1
	echo.
	call :c 03 " ══════════► ESTADO  : "
	bcdedit.exe -set TESTSIGNING ON >nul 2>&1
	call :c 03 "LISTO"
  echo.	
  echo.
	call :c 27 "  REINICIAR PC PARA COMPLETAR LOS CAMBIOS"
	echo.
	pause >nul 2>&1
	goto:inicio

:op3
echo.
  echo.
	echo.
	call :c 0E " ══════════► ABRIENDO	: " 
	powershell wget https://github.com/joseph-nc/IDM_ACTIVADOR/releases/download/V1.0/idm_activador.bat -OutFile C:\idm_activador.bat >nul 2>&1
	start "" C:\idm_activador.bat & exit >nul 2>&1
  echo.

:op4
echo.
  echo.
	echo.
	call :c 0E " ══════════► ABRIENDO	: " 
	powershell wget https://github.com/joseph-nc/KSM-WINDOWS-OFFICE-ACTIVADOR/releases/download/2.0/actwin.bat -OutFile "" C:\actwin.bat >nul 2>&1
	start "" C:\actwin.bat & exit >nul 2>&1
	echo.

:op6
color 1
cls
echo.
echo.
echo  █████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗
echo  ╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[1: DRIVERS QUALCOMM]░░░░░░░░░░░░[7: DRIVERS HUAWEI/HONOR]░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[2: DRIVERS MEDIATEK]░░░░░░░░░░░░[8: DRIVERS XIAOMI]░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[3: DRIVERS SPECTRUM]░░░░░░░░░░░░[9: DRIVERS LIBUSB]░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[4: DRIVERS SAMSUNG]░░░░░░░░░░░░░[A: ALL DRIVERS (PACK)]░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[5: DRIVERS OPPO]░░░░░░░░░░░░░░░░[B: INICIO]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░[6: DRIVERS MOTOROLA]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ╚═╝░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░╚═╝
echo  █████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗
echo  ╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝
call :c 03 "  ║ "
echo.
call :c 03 "  ╚════════════════════════►  SELECCIONE UNA OPCION [ESCRIBE EL NUMERO]:"
choice /C 123456789AB /N
::choice /C 123456789A /M "  ╚══════════════════════►  SELECCIONE UNA OPCION "
goto option-%errorlevel%
:option-1 QCM
goto:QCM
:option-2 MTK
goto:MTK
:option-3 SPD
goto:SPD
:option-4 SAMS
goto:SAMS
:option-5 OPPO
:goto:OPPO
:option-6 MOTO
goto:MOTO
:option-7 HUA
goto:HUA
:option-8 XIA
goto:XIA
:option-9 LIB
goto:LIB
:option-10 ALL
goto:All
:option-11 ATRAS
goto:ATRAS

:ATRAS
echo.
goto:inicio
echo.

:QCM
echo.
    start "" https://github.com/joseph-nc/DRIVERS-ANDROID/releases/download/V1/DRIVER.QUALCOMM.rar
    echo.
goto:op6

:MTK
echo.
    start "" https://github.com/joseph-nc/DRIVERS-ANDROID/releases/download/V1/MTK.DRIVER.rar
    echo.
goto:op6

:SPD
echo.
    start "" https://github.com/joseph-nc/DRIVERS-ANDROID/releases/download/V1/DRIVER.SPRD.rar
    echo.
goto:op6

:SAMS
echo.
    start "" https://github.com/joseph-nc/DRIVERS-ANDROID/releases/download/V1/SAMSUNG.DRIVER.rar
    echo.
goto:op6

:MOTO
echo.
    start "" https://github.com/joseph-nc/DRIVERS-ANDROID/releases/download/V1/MOTOROLA.DRIVER.rar
    echo.
goto:op6

:OPPO
echo.
    start "" https://github.com/joseph-nc/DRIVERS-ANDROID/releases/download/V1/OPPO.DRIVER.rar
    echo.
goto:op6

:HUA
echo.
    start "" https://github.com/joseph-nc/DRIVERS-ANDROID/releases/download/V1/DRIVER.HUAWEI.HONOR.rar
    echo.
goto:op6

:XIA
echo.
    start "" https://github.com/joseph-nc/DRIVERS-ANDROID/releases/download/V1/XIAOMI.DRIVER.rar
    echo.
goto:op6

:LIB
echo.
    start "" https://github.com/joseph-nc/DRIVERS-ANDROID/releases/download/V1/libusb-win32-devel-filter-1.2.6.0.rar
    echo.
goto:op6

:ALL
echo.
    start "" https://github.com/joseph-nc/DRIVERS-ANDROID/releases/download/V1/DRIVERS_ANDROID.rar
    echo.
goto:op6

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:op7
echo.
	start "" scrcpy\scrcpy.exe
echo.
goto:inicio

:op8
echo.
    start "" https://joseph-nc.github.io/gsmtools.github.io/
    echo.
goto:inicio

:op9
echo.
	SET /p modelo= ^> ══════════► ESCRIBA EL MODELO (EJ: A325M): 
	start "" https://samfw.com/firmware/SM-%modelo%
  echo.
goto:inicio

:op10
color 05
cls
echo  █████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗
echo  ╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓[ A     : TELEGRAM]▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓[ B     : WHATSAPP]▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓[ C     : FACEBOOK]▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓[ D     : DONAR :)]▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║▓▓▓[CUALQUIER SUGERENCIA ES BIENVENIDA]▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╚{ 0:  INICIO}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██║
echo  ██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║
echo  ╚═╝▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌▐░▌╚═╝
echo  █████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗
echo  ╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝
echo   ║
echo   ║
SET /p var= ^> ╚════════════════════════►  SELECCIONE UNA OPCION [ESCRIBE EL NUMERO]: 

if "%var%"=="A" goto opA
if "%var%"=="B" goto opB
if "%var%"=="C" goto opC
if "%var%"=="D" goto opD
if "%var%"=="a" goto opA
if "%var%"=="b" goto opB
if "%var%"=="c" goto opC
if "%var%"=="d" goto opD
if "%var%"=="0" goto op0

echo. El numero "%var%" no es una opcion valida, por favor intente de nuevo.
echo.
pause
echo.
goto:op10

:op0

echo.
goto:inicio
echo.

:opA

echo.
echo.
	start "" https://t.me/degnansolution
echo.
goto:op10

:opB

echo.
start "" https://wa.me/447535257683
echo.
goto:op10

:opC

echo.
start "" https://www.facebook.com/degnanf
echo.
goto:op10

:opD

echo.
start "" https://www.buymeacoffee.com/degnanf
echo.
goto:op10


:op11
echo.
	call :c 0E " ══════════► PROCESO		: "
    call :c 0C "DISABLE UPDATES SAMSUNG - OPPO - MI"
	echo.
	echo.
		call :adbreadinfo
			if "%brand%"=="samsung" (goto up1) else (
			if "%brand%"=="OPPO" (goto up2) else (
			if "%brand%"=="Xiaomi" (goto up3) else (goto up0)))
		:up1
		echo.
		call :c 0E " ══════════► DESACTIVANDO UPDATES	: "
		adb shell pm disable-user --user 0 com.wssyncmldm >nul 2>&1
		adb shell pm disable-user --user 0 com.sec.android.soagent >nul 2>&1
		call :c 0A "LISTO"
    echo.
	echo.
    pause
    goto:inicio

		:up2
		echo.
		call :c 0E " ══════════► DESACTIVANDO UPDATES	: "
		adb shell pm uninstall -k --user 0 com.oppo.ota >NUL
		adb shell pm uninstall -k --user 0 com.oppo.otaui >NUL
		call :c 0A "LISTO"
    echo.
	echo.
	echo.
    pause
goto:inicio	
	
		:up3
		echo.
		call :c 0E " ══════════► DESACTIVANDO UPDATES	: "
		adb shell pm uninstall -k -usuario 0 com.android.updater >NUL
		call :c 0A "LISTO"
    echo.
	echo.
	echo.
    pause
goto:inicio

        :up0
		echo.
		call :c 0E " ══════════► DESACTIVANDO		: "
		adb shell pm disable-user --user 0 com.wssyncmldm >NUL
		adb shell pm disable-user --user 0 com.sec.android.soagent >NUL
		call :c 0A "LISTO"
    echo.
	echo.
	echo.
    pause
goto:inicio


:op12
echo.
		start main.exe
	echo.
	call :c 0E " ══════════►           SI NO SE ACTIVA ADB VOLVER A INTENTAR. "
	echo.
	call :c 0E "                     [PRECIONA CUALQUIER TECLA PARA CONTINUAR] "
	echo.
pause >nul
goto:inicio
:op13
echo.
	call :c 0E " ══════════► PROCESO		: "
    call :c 0C "ACTIVAR PUERTO DIAG"
	echo.
	echo.
	call :c 0E " ══════════► PIDIENDO PERMISOS ROOT	: "	
	for /f "delims=" %%a in ('adb shell "su -c whoami"') do set "rootstatus=%%a"
			if "%rootstatus%"=="root" (goto:puertodiag) else (goto:noroot)
goto:inicio			
		:puertodiag
		call :c 0C "LISTO"
		echo.
		echo.
		call :adbreadinfo
		echo.
		call :c 0E " ACTIVANDO PUERTO DIAG	: "
		@adb shell "su -c setprop sys.usb.config diag,adb" >NUL 2>&1
		call :c 0A "LISTO"
		echo.	
		echo.
		echo.
    pause
goto:inicio

:op14
goto:soon


::::::::::::::DEFENDER REMOVE


:--------------------------------------
:: Arguments Section
IF "%1"== NUL GOTO :menu
IF "%1"== "/y" GOTO :removedef
IF "%1"== "/Y" GOTO :removedef
IF "%1"== "/N" GOTO :tweaksdef
IF "%1"== "/n" GOTO :tweaksdef
IF "%1"== "/e" GOTO :enabledefanti
IF "%1"== "/E" GOTO :enabledefanti
IF "%1"== "/M" GOTO :tweaksdefanti
IF "%1"== "/m" GOTO :tweaksdefanti
IF "%1"== "/R" GOTO :enabledef
IF "%1"== "/r" GOTO :enabledef
:--------------------------------------

:--------------------------------------
:menu
cls
echo --------------------------Defender Remover Script------------------------------------
echo #####################################################################################
call :c 04 "              IMPORTANTE: " &call :c 05 " DAR PERMISOS DE ADMINISTRADOR CUANDO"
echo.
call :c 05 " SE SOLICITE LAS VECES QUE PIDA, YA QUE CASA PERMISO HACE UN PROCESO DISTINTO"
echo.
echo #####################################################################################
echo.
echo Select an option:
echo.
echo Press (Y) for removing Defender and Security Components 
echo (old method, breaking Windows Updates/UWP in some version of Windows, 
echo removes files and unregisters classes)
echo.
echo Press (N) for disabling Defender and Security Components (safe)
echo Press (M) for disabling Defender Antivirus only (safe)
echo Press (E) for enabling Defender (restore actions where M is pressed)
echo Press (R) for enabling Defender and Security Components (restore actions where N is pressed)
echo.
set /P c=Select one of the options to continue: 

:: Check if the input is one of the valid keys
if /I "%c%" EQU "Y" goto :removedef
if /I "%c%" EQU "N" goto :tweaksdef
if /I "%c%" EQU "E" goto :enabledefanti
if /I "%c%" EQU "M" goto :tweaksdefanti
if /I "%c%" EQU "R" goto :enabledef

:: If none of the valid keys are pressed, do nothing
goto :eof
:--------------------------------------
:--------------------------------------
:removedef
cls
echo Killing Tasks...
for /f "delims=" %%i in (Remover\TKL.txt) do (taskkill.exe /f /im "%%i") >nul
cls
echo Removing Windows Security UWP...
for /d %%f in ("C:\Program Files\WindowsApps\Microsoft.SecHealthUI*") do (PowerRun.exe cmd.exe /c rmdir /s /q "%%f") >nul
cls
echo Applying Registry Files...
for /r %%k in (Remover\REGS\*.reg) do (PowerRun.exe regedit.exe /s "%%k") >nul
cls
echo Removing Windows Defender/Security Components Files...
for /f "delims=" %%i in (Remover\FDL.txt) do (PowerRun.exe cmd.exe /c del /f /q "%%i") 1>nul
for /f "delims=" %%i in (Remover\DDL.txt) do (PowerRun.exe cmd.exe /c rmdir /s /q "%%i") >nul
timeout /t 5 /nobreak
shutdown /r /f /t 0
goto :eof
:--------------------------------------


:--------------------------------------
:image
start /wait ISOCreator.cmd
goto :eof
:--------------------------------------

:--------------------------------------

:tweaksdef
CLS & echo Disable Defender and Security Components...
:: Disable Defender's Scheduled Tasks
PowerRun cmd.exe /k "schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cache Maintenance" /Disable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cleanup" /Disable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan" /Disable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Verification" /Disable"
PowerRun.exe regedit.exe /s "DisablerS\Disable.reg" >nul
PowerRun cmd.exe /k "taskkill /f /im smartscreen.exe & taskkill /f /im MsMpEngCP.exe & taskkill /f /im MsMpEng.exe"
PowerRun.exe cmd.exe /c move /y "C:\ProgramData\Microsoft\Windows Defender" "C:\ProgramData\Microsoft\Windows Defender Ma"
PowerRun.exe cmd.exe /c move /y "C:\ProgramData\Microsoft\Windows Defender Advanced Threat Protection" "C:\ProgramData\Microsoft\Windows Defender Advanced Threat Protection Ma"
PowerRun.exe cmd.exe /c move /y "C:\Program Files\Windows Defender" "C:\Program Files\Windows Defender Ma"
PowerRun.exe cmd.exe /c move /y "C:\Program Files\Windows Defender Advanced Threat Protection" "C:\Program Files\Windows Defender Advanced Threat Protection Ma"
PowerRun.exe cmd.exe /c move /y "C:\Program Files (x86)\Windows Defender" "C:\Program Files (x86)\Windows Defender Ma"
PowerRun.exe cmd.exe /c move /y "C:\Windows\System32\smartscreen.exe" "C:\Windows\System32\smartscreen.plm"
cls & echo Antivirus and Security Components Disabled. A reboot is needed!
timeout /t 5 /nobreak
shutdown /r /f /t 0
goto :eof
:--------------------------------------

:--------------------------------------
:enabledef
CLS & echo Enable Defender and Security Components...
:: Enable Defender's Scheduled Tasks
PowerRun cmd.exe /k "schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cache Maintenance" /Enable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cleanup" /Enable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan" /Enable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Verification" /Enable"
PowerRun.exe regedit.exe /s "DisablerS\Enable.reg"
PowerRun.exe cmd.exe /c move /y "C:\ProgramData\Microsoft\Windows Defender Ma" "C:\ProgramData\Microsoft\Windows Defender"
PowerRun.exe cmd.exe /c move /y "C:\ProgramData\Microsoft\Windows Defender Advanced Threat Protection Ma" "C:\ProgramData\Microsoft\Windows Defender Advanced Threat Protection"
PowerRun.exe cmd.exe /c move /y "C:\Program Files\Windows Defender Ma" "C:\Program Files\Windows Defender"
PowerRun.exe cmd.exe /c move /y "C:\Program Files\Windows Defender Advanced Threat Protection Ma" "C:\Program Files\Windows Defender Advanced Threat Protection"
PowerRun.exe cmd.exe /c move /y "C:\Program Files (x86)\Windows Defender Ma" "C:\Program Files (x86)\Windows Defender"
PowerRun.exe cmd.exe /c move /y "C:\Windows\System32\smartscreen.plm" "C:\Windows\System32\smartscreen.exe"
cls & echo Antivirus and Windows Security Components Enabled. A reboot is needed!
timeout /t 5 /nobreak
shutdown /r /f /t 0
goto :eof
:--------------------------------------

:tweaksdefanti
CLS & echo Disabling Defender...
:: Disable Defender's Scheduled Tasks
PowerRun cmd.exe /k "schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cache Maintenance" /Disable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cleanup" /Disable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan" /Disable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Verification" /Disable"
PowerRun.exe regedit.exe /s "Disabler\Disable.reg" >nul
PowerRun cmd.exe /k "taskkill /f /im smartscreen.exe & taskkill /f /im MsMpEngCP.exe & taskkill /f /im MsMpEng.exe"
PowerRun.exe cmd.exe /c move /y "C:\ProgramData\Microsoft\Windows Defender" "C:\ProgramData\Microsoft\Windows Defender Ma"
PowerRun.exe cmd.exe /c move /y "C:\ProgramData\Microsoft\Windows Defender Advanced Threat Protection" "C:\ProgramData\Microsoft\Windows Defender Advanced Threat Protection Ma"
PowerRun.exe cmd.exe /c move /y "C:\Program Files\Windows Defender" "C:\Program Files\Windows Defender Ma"
PowerRun.exe cmd.exe /c move /y "C:\Program Files\Windows Defender Advanced Threat Protection" "C:\Program Files\Windows Defender Advanced Threat Protection Ma"
PowerRun.exe cmd.exe /c move /y "C:\Program Files (x86)\Windows Defender" "C:\Program Files (x86)\Windows Defender Ma"
PowerRun.exe cmd.exe /c move /y "C:\Windows\System32\smartscreen.exe" "C:\Windows\System32\smartscreen.plm"
cls & echo Antivirus disabled. A reboot is needed!
timeout /t 5 /nobreak
shutdown /r /f /t 2
goto :eof
:--------------------------------------

:--------------------------------------
:enabledefanti
CLS & echo Enable Defender...
:: Enable Defender's Scheduled Tasks
PowerRun cmd.exe /k "schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cache Maintenance" /Enable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cleanup" /Enable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan" /Enable & schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Verification" /Enable"
PowerRun.exe regedit.exe /s "Disabler\Enable.reg"
PowerRun.exe cmd.exe /c move /y "C:\ProgramData\Microsoft\Windows Defender Ma" "C:\ProgramData\Microsoft\Windows Defender"
PowerRun.exe cmd.exe /c move /y "C:\ProgramData\Microsoft\Windows Defender Advanced Threat Protection Ma" "C:\ProgramData\Microsoft\Windows Defender Advanced Threat Protection"
PowerRun.exe cmd.exe /c move /y "C:\Program Files\Windows Defender Ma" "C:\Program Files\Windows Defender"
PowerRun.exe cmd.exe /c move /y "C:\Program Files\Windows Defender Advanced Threat Protection Ma" "C:\Program Files\Windows Defender Advanced Threat Protection"
PowerRun.exe cmd.exe /c move /y "C:\Program Files (x86)\Windows Defender Ma" "C:\Program Files (x86)\Windows Defender"
PowerRun.exe cmd.exe /c move /y "C:\Windows\System32\smartscreen.plm" "C:\Windows\System32\smartscreen.exe"
cls & echo Antivirus Enabled. A reboot is needed!
timeout /t 5 /nobreak
shutdown /r /f /t 0
:--------------------------------------

:--------------------------------------
:eof
:: End of script, do nothing
exit
:--------------------------------------


:soon
echo.
echo.
echo -------------------------------------------------------------------------------------
echo.
echo     ____  ___   __  __  ___  _   _   ____   ____    ___    ___   _   _ 
echo    / ___^|/ _ \ ^|  \/  ^|^|_ _^|^| \ ^| ^| / ___^| / ___^|  / _ \  / _ \ ^| \ ^| ^|
echo   ^| ^|   ^| ^| ^| ^|^| ^|\/^| ^| ^| ^| ^|  \^| ^|^| ^|  _  \___ \ ^| ^| ^| ^|^| ^| ^| ^|^|  \^| ^|
echo   ^| ^|___^| ^|_^| ^|^| ^|  ^| ^| ^| ^| ^| ^|\  ^|^| ^|_^| ^|  ___) ^|^| ^|_^| ^|^| ^|_^| ^|^| ^|\  ^|
echo    \____^|\___/ ^|_^|  ^|_^|^|___^|^|_^| \_^| \____^| ^|____/  \___/  \___/ ^|_^| \_^|
echo.
echo --------------------------------------------------------------------------------------
pause
goto:inicio
:noroot
		echo.
		call :c 0E "  ********************************************"
		echo.
		call :c 0E "  *    EL EQUIPO DEBE ESTAR ROOTEADO         *"
		echo.
		call :c 0E "  *    ROOTEE O ENTREGUE PERMISOS SHELL      *"
		echo.
		call :c 0E "  ********************************************"
		echo.
		echo.
		echo.
	pause
goto:inicio

:fastbootreadxiaomi
		fastboot devices -l | find "fastboot" >nul
		if errorlevel 1 (
			goto:fastbootreadnc
		) else (
			goto:fastbootreadmi1
		)
		:fastbootreadmi1
		call :c 0E " DECTECTANDO PROCESADOR	: "
		set "cpudetect= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar kernel 2^>^&1 ^| findstr kernel') do set "cpudetect=%%a" >nul
		if "%cpudetect%"=="lk" (
			goto:fastbootreadmimtk
		) else (
			goto:fastbootreadmiqcom
				)
		)
		:fastbootreadmiqcom
		call :c 0C "QUALCOMM"
		echo. 
		set "codename= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar product 2^>^&1 ^| findstr product') do set "codename=%%a"
		set "serialno= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar serialno 2^>^&1 ^| findstr serialno') do set "serialno=%%a"
		set "memorytype= "
		for /f "tokens=2-3 delims=: " %%a in ('fastboot getvar variant 2^>^&1 ^| findstr variant') do set "memorytype=%%a %%b"
		set "bootloaderlock= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar unlocked 2^>^&1 ^| findstr unlocked') do set "bootloaderlock=%%a"
		if "%bootloaderlock%"=="no" (set "bootloaderlock=LOCKED") else (set "bootloaderlock=UNLOCKED")
		set "hwrev= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar hw-revision 2^>^&1 ^| findstr hw-revision') do set "hwrev=%%a"
		set "boardver= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar board_version 2^>^&1 ^| findstr board_version') do set "boardver=%%a"
		set "slotsim= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar slot-count 2^>^&1 ^| findstr slot-count') do set "slotsim=%%a"
		set "sistemab= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar current-slot 2^>^&1 ^| findstr current-slot') do set "sistemab=%%a"
		set "arb= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar anti 2^>^&1 ^| findstr anti') do set "arb=%%a"
		set "frpmi= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar frp 2^>^&1 ^| findstr frp') do set "frpmi=%%a"
		echo.
		call :c 0E " CODENAME		: "&call :c 06 "%codename%"
		echo.
		call :c 0E " SERIAL NUMBER		: "&call :c 06 "%serialno%"
		echo.
		call :c 0E " IP PUBLICA		: "&call :c 06 "%ippublica%"
		echo.
		call :c 0E " TIPO DE MEMORIA	: "&call :c 06 "%memorytype%"
		echo.
		call :c 0E " BOOTLOADER		: "&call :c 06 "%bootloaderlock%"
		echo.
		call :c 0E " BOARD VERSION		: "&call :c 06 "%boardver%"
		echo.
		call :c 0E " REV HARDWARE		: "&call :c 06 "%hwrev%"
		echo.
		call :c 0E " SLOT SIM		: "&call :c 06 "%slotsim%"
		echo.
		call :c 0E " ANTIROLLBACK		: "&call :c 06 "%arb%"
		echo.
		call :c 0E " FRP			: "&call :c 06 "%frpmi%"
		echo.
		exit/b
		
		:fastbootreadmimtk
		call :c 0C "MEDIATEK"
		echo. 
		set "codename= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar product 2^>^&1 ^| findstr product') do set "codename=%%a"
		set "serialno= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar serialno 2^>^&1 ^| findstr serialno') do set "serialno=%%a"
		set "frpmi= "
		for /f "tokens=1-3 delims=: " %%a in ('fastboot getvar has-slot:frp 2^>^&1 ^| findstr has-slot:frp') do set "frpmi=%%c"
		set "bootloaderlock= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar unlocked 2^>^&1 ^| findstr unlocked') do set "bootloaderlock=%%a"
		if "%bootloaderlock%"=="no" (set "bootloaderlock=LOCKED") else (set "bootloaderlock=UNLOCKED")
		set "hwrev= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar hw-revision 2^>^&1 ^| findstr hw-revision') do set "hwrev=%%a"
		set "slotsim= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar slot-count 2^>^&1 ^| findstr slot-count') do set "slotsim=%%a"
		set "arb= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar anti 2^>^&1 ^| findstr anti') do set "arb=%%a"
		set "sistemab= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar current-slot 2^>^&1 ^| findstr current-slot') do set "sistemab=%%a"
		echo.
		call :c 0E " CODENAME		: "&call :c 06 "%codename%"
		echo.
		call :c 0E " SERIAL NUMBER		: "&call :c 06 "%serialno%"
		echo.
		call :c 0E " IP PUBLICA		: "&call :c 06 "%ippublica%"
		echo.
		call :c 0E " SLOT SISTEMA		: "&call :c 06 "%sistemab%"
		echo.
		call :c 0E " BOOTLOADER		: "&call :c 06 "%bootloaderlock%"
		echo.
		call :c 0E " REV HARDWARE		: "&call :c 06 "%hwrev%"
		echo.
		call :c 0E " SLOT SIM		: "&call :c 06 "%slotsim%"
		echo.
		call :c 0E " ANTIROLLBACK		: "&call :c 06 "%arb%"
		echo.
		call :c 0E " FRP			: "&call :c 06 "%frpmi%"
		echo.
		exit/b
		
:fastbootreadmoto
		fastboot devices -l | find "fastboot" >nul
		if errorlevel 1 (
			goto:fastbootreadnc
		) else (
			goto:fastbootreadmoto1
		)
		:fastbootreadmoto1
		call :c 0E " DECTECTANDO PROCESADOR	: "
		set "cpudetect= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar kernel 2^>^&1 ^| findstr kernel') do set "cpudetect=%%a" >nul
		if "%cpudetect%"=="lk" (
			goto:fastbootreadmotomtk
		) else (
		set "cid= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar cid 2^>^&1 ^| findstr cid') do set "cid=%%a" >nul
		if not "cid"==" " (
			goto:fastbootreadmotoqcom
		) else (
			goto:fastbootreadmotospd
				)
		)
		:fastbootreadmotoqcom
		call :c 0C "QUALCOMM"
		echo. 
		set "codename= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar product 2^>^&1 ^| findstr product') do set "codename=%%a"
		set "serialno= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar serialno 2^>^&1 ^| findstr serialno') do set "serialno=%%a"
		set "memorytype= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar storage-type 2^>^&1 ^| findstr storage-type') do set "memorytype=%%a"
		set "bootloaderlock= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar unlocked 2^>^&1 ^| findstr unlocked') do set "bootloaderlock=%%a"
		set "carrierid= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar ro.carrier 2^>^&1 ^| findstr ro.carrier') do set "carrierid=%%a"
		set "slotsim= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar slot-count 2^>^&1 ^| findstr slot-count') do set "slotsim=%%a"
		set "modelo= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar sku 2^>^&1 ^| findstr sku') do set "modelo=%%a"
		set "imeimoto= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar imei 2^>^&1 ^| findstr imei') do set "imeimoto=%%a"
		set "frpmoto= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar frp-state 2^>^&1 ^| findstr frp-state') do set "frpmoto=%%a"
		set "idbat= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar battid 2^>^&1 ^| findstr battid') do set "idbat=%%a"
		set "cidmoto= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar cid 2^>^&1 ^| findstr cid') do set "cidmoto=%%a"
		set "cpumoto= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar cpu 2^>^&1 ^| findstr cpu') do set "cpumoto=%%a"
		set "sistemab= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar current-slot 2^>^&1 ^| findstr current-slot') do set "sistemab=%%a"
		set "emmcmoto= "
		for /f "tokens=2-3 delims=: " %%a in ('fastboot getvar emmc 2^>^&1 ^| findstr emmc') do set "emmcmoto=%%a %%b"
		set "rammoto= "
		for /f "tokens=2-3 delims=: " %%a in ('fastboot getvar ram 2^>^&1 ^| findstr ram') do set "rammoto=%%a %%b"
		echo.
		call :c 0E " MODELO			: "&call :c 06 "%modelo%"
		echo.
		call :c 0E " SERIAL NUMBER		: "&call :c 06 "%serialno%"
		echo.
		call :c 0E " IMEI			: "&call :c 06 "%imeimoto%"
		echo.
		call :c 0E " IP PUBLICA		: "&call :c 06 "%ippublica%"
		echo.
		call :c 0E " TIPO DE MEMORIA	: "&call :c 06 "%memorytype%"
		echo.
		call :c 0E " ALMACENAMIENTO		: "&call :c 06 "%emmcmoto%"
		echo.
		call :c 0E " RAM			: "&call :c 06 "%rammoto%"
		echo.
		call :c 0E " CPU			: "&call :c 06 "%cpumoto%"
		echo.
		call :c 0E " CID			: "&call :c 06 "%cidmoto%"
		echo.
		call :c 0E " BOOTLOADER 		: "&call :c 06 "%bootloaderlock%"
		echo.
		call :c 0E " ID BATERIA		: "&call :c 06 "%idbat%"
		echo.
		call :c 0E " SLOT SIM		: "&call :c 06 "%slotsim%"
		echo.
		call :c 0E " CODENAME		: "&call :c 06 "%codename%"
		echo.
		call :c 0E " CARRIER ID		: "&call :c 06 "%carrierid%"
		echo.
		call :c 0E " FRP			: "&call :c 06 "%frpmoto%"
		echo.
		echo.
		echo.
		echo off | clip
		(
		echo IP PUB: %ippublica%
		echo SN: %serialno%
		echo MODELO: %modelo%
		echo IMEI: %imeimoto%
		)| clip
		call :c 0E " SE HA COPIADO IP, SN, MODELO E IMEI EN EL PORTAPAPELES"
		
		exit/b
		
		:fastbootreadmotomtk
		call :c 0C "MEDIATEK"
		echo. 
		set "codename= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar product 2^>^&1 ^| findstr product') do set "codename=%%a"
		set "serialno= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar serialno 2^>^&1 ^| findstr serialno') do set "serialno=%%a"
		set "memorytype= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar variant 2^>^&1 ^| findstr variant') do set "memorytype=%%a"
		set "bootloaderlock= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar unlocked 2^>^&1 ^| findstr unlocked') do set "bootloaderlock=%%a"
		if "%bootloaderlock%"=="no" (set "bootloaderlock=LOCKED") else (set "bootloaderlock=UNLOCKED")
		set "carrierid= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar ro.carrier.ontim 2^>^&1 ^| findstr ro.carrier.ontim') do set "carrierid=%%a"
		set "slotsim= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar slot-count 2^>^&1 ^| findstr slot-count') do set "slotsim=%%a"
		set "modelo= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar ro.boot.hardware.sku 2^>^&1 ^| findstr ro.boot.hardware.sku') do set "modelo=%%a"
		set "sistemab= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar current-slot 2^>^&1 ^| findstr current-slot') do set "sistemab=%%a"
		set "frpmoto= "
		for /f "tokens=1-3 delims=: " %%a in ('fastboot getvar has-slot:frp 2^>^&1 ^| findstr has-slot:frp') do set "frpmoto=%%c"
		echo.
		call :c 0E " MODELO			: "&call :c 06 "%modelo%"
		echo.
		call :c 0E " SERIAL NUMBER		: "&call :c 06 "%serialno%"
		echo.
		call :c 0E " IP PUBLICA		: "&call :c 06 "%ippublica%"
		echo.
		call :c 0E " BOOTLOADER 		: "&call :c 06 "%bootloaderlock%"
		echo.
		call :c 0E " SLOT SIM		: "&call :c 06 "%slotsim%"
		echo.
		call :c 0E " CODENAME		: "&call :c 06 "%codename%"
		echo.
		call :c 0E " CARRIER ID		: "&call :c 06 "%carrierid%"
		echo.
		call :c 0E " SLOT SISTEMA		: "&call :c 06 "%sistemab%"
		echo.
		call :c 0E " FRP			: "&call :c 06 "%frpmoto%"
		echo.
		echo.
		echo.
		echo off | clip
		(
		echo MODELO: %modelo%
		echo SN: %serialno%
		echo IP PUB: %ippublica%
		)| clip
		call :c 0E " SE HA COPIADO MODELO, SN, IP EN EL PORTAPAPELES"
		exit/b
		
		:fastbootreadmotospd
		call :c 0C "SPREADTRUM"
		echo. 
		set "codename= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar product 2^>^&1 ^| findstr product') do set "codename=%%a"
		set "carrierid= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar ro.carrier.ontim 2^>^&1 ^| findstr ro.carrier.ontim') do set "carrierid=%%a"
		set "modelo= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar sku 2^>^&1 ^| findstr sku') do set "modelo=%%a"
		set "imeimoto= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar imei 2^>^&1 ^| findstr imei') do set "imeimoto=%%a"
		set "slotsim= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar persist.radio.multisim.config 2^>^&1 ^| findstr persist.radio.multisim.config') do set "slotsim=%%a"
		echo.
		call :c 0E " MODELO			: "&call :c 06 "%modelo%"
		echo.
		call :c 0E " SERIAL NUMBER		: "&call :c 06 "%serialno%"
		echo.
		call :c 0E " IMEI			: "&call :c 06 "%imeimoto%"
		echo.
		call :c 0E " IP PUBLICA		: "&call :c 06 "%ippublica%"
		echo.
		call :c 0E " SLOT SIM		: "&call :c 06 "%slotsim%"
		echo.
		call :c 0E " CODENAME		: "&call :c 06 "%codename%"
		echo.
		echo.
		echo.
		echo off | clip
		(
		echo MODELO: %modelo%
		echo SN: %serialno%
		echo IMEI: %imeimoto%
		echo IP PUB: %ippublica%
		)| clip
		call :c 0E " SE HA COPIADO MODELO, SN, IMEI, IP EN EL PORTAPAPELES"
		exit/b
		
:fastbootreadnc
		call :c 0E "  *******************************************************************"
		echo.
		call :c 0E "  * DISPOSITIVO NO DETECTADO, FAVOR CONECTE EL EQUIPO EN FASTBOOT   *"
		echo.
		call :c 0E "  *******************************************************************"
		echo.
		echo.
		echo.
	pause
goto:inicio

		:fastbootreadhuawei
		echo. 
		set "build= "
		for /f "tokens=2-3 delims=: " %%a in ('fastboot oem get-build-number 2^>^&1 ^| findstr bootloader') do set "build=%%a %%b"
		set "serialno= "
		for /f "tokens=1 delims=	" %%a in ('fastboot devices 2^>^&1 ^| findstr fastboot') do set "serialno=%%a"
		set "keyversion= "
		for /f "tokens=2 delims=) " %%a in ('fastboot oem get_key_version 2^>^&1 ^| findstr bootloader') do set "keyversion=%%a"
		set "bootloaderlock= "
		for /f "tokens=2 delims=) " %%a in ('fastboot oem get-bootinfo 2^>^&1 ^| findstr bootloader') do set "bootloaderlock=%%a"
		set "modelo= "
		for /f "tokens=2 delims=) " %%a in ('fastboot oem get-product-model 2^>^&1 ^| findstr bootloader') do set "modelo=%%a"
		set "androidv= "
		for /f "tokens=2 delims=:" %%a in ('fastboot oem oeminforead-ANDROID_VERSION 2^>^&1 ^| findstr bootloader') do set "androidv=%%a"
		set "fblock= "
		for /f "tokens=2-4 delims=: " %%a in ('fastboot oem lock-state info 2^>^&1 ^| findstr FB') do set "fblock=%%c"
		set "userlock= "
		for /f "tokens=2-4 delims=: " %%a in ('fastboot oem lock-state info 2^>^&1 ^| findstr USER') do set "userlock=%%c"
		set "idbat= "
		for /f "tokens=2 delims=) " %%a in ('fastboot oem battery_present_check 2^>^&1 ^| findstr bootloader') do set "idbat=%%a"
		set "vendorcountry= "
		for /f "tokens=2 delims=: " %%a in ('fastboot getvar vendorcountry 2^>^&1 ^| findstr vendorcountry') do set "vendorcountry=%%a"
		set "baseversion= "
		for /f "tokens=2-3 delims=: " %%a in ('fastboot oem oeminforead-BASE_VERSION 2^>^&1 ^| findstr bootloader') do set "baseversion=%%a %%b"
		set "customversion= "
		for /f "tokens=2-3 delims=: " %%a in ('fastboot oem oeminforead-CUSTOM_VERSION 2^>^&1 ^| findstr bootloader') do set "customversion=%%a %%b"
		set "preloadversion= "
		for /f "tokens=2-3 delims=: " %%a in ('fastboot oem oeminforead-PRELOAD_VERSION 2^>^&1 ^| findstr bootloader') do set "preloadversion=%%a %%b"
		echo.
		call :c 0E " MODELO			: "&call :c 06 "%modelo%"
		echo.
		call :c 0E " SERIAL NUMBER		: "&call :c 06 "%serialno%"
		echo.
		call :c 0E " BUILD NUMBER		: "&call :c 06 "%build%"
		echo.
		call :c 0E " VENDOR/COUNTRY		: "&call :c 06 "%vendorcountry%"
		echo.
		call :c 0E " KEY VERSION		: "&call :c 06 "%keyversion%"
		echo.
		call :c 0E " BOOTLOADER 		: "&call :c 06 "%bootloaderlock%"
		echo.
		call :c 0E " ID BATERIA		: "&call :c 06 "%idbat%"
		echo.
		call :c 0E " ANDROID		: "&call :c 06 "%androidv%"
		echo.
		call :c 0E " FB LOCKSTATE		: "&call :c 06 "%fblock%"
		echo.
		call :c 0E " USER LOCKSTATE		: "&call :c 06 "%userlock%"		
		echo.
		call :c 0E " BASE VERSION		: "&call :c 06 "%baseversion%"
		echo.
		call :c 0E " CUSTOM VERSION		: "&call :c 06 "%customversion%"
		echo.
		call :c 0E " PRELOAD VERSION	: "&call :c 06 "%preloadversion%"
		echo.
		echo.
		
		exit/b


:adbreadinfo
		adb devices -l | find "device product:" >nul 2>&1
		if errorlevel 1 (
			goto:adbreadnc
		) else (
			goto:adbread
		)
		:adbread
		set "modelo= "
		for /f "delims=" %%a in ('adb shell getprop ro.product.model') do set "modelo=%%a"
		set "build= "
		for /f "delims=" %%a in ('adb shell getprop ro.build.version.incremental') do set "build=%%a"
		set "version= "
		for /f "delims=" %%a in ('adb shell getprop ro.build.version.release') do set "version=%%a"
		set "modem= "
		for /f "delims=" %%a in ('adb shell getprop gsm.version.baseband') do set "modem=%%a"
		set "knox= "
		for /f "delims=" %%a in ('adb shell getprop knox.kg.state') do set "knox=%%a"
		set "chip= "
		for /f "delims=" %%a in ('adb shell getprop ro.hardware.chipname') do set "chip=%%a"
		set "sn= "
		for /f "delims=" %%a in ('adb get-serialno') do set "sn=%%a"
		set "imei= "
		for /f "delims=" %%a in ('adb shell "service call iphonesubinfo 1 | cut -c 52-66 | tr -d '.[:space:]'"') do set "imei=%%a"
		set "security= "
		for /f "delims=" %%a in ('adb shell getprop ro.build.version.security_patch') do set "security=%%a"
		set "csc= "
		for /f "delims=" %%a in ('adb shell getprop ro.csc.omcnw_code') do set "csc=%%a"
		set "carrierid= "
		for /f "delims=" %%a in ('adb shell getprop ro.boot.carrierid') do set "carrierid=%%a"
		set "brand= "
		for /f "delims=" %%a in ('adb shell getprop ro.product.manufacturer') do set "brand=%%a"
		set "simstate= "
		for /f "delims=" %%a in ('adb shell getprop gsm.sim.state') do set "simstate=%%a"
	    set "manufactura= "
		for /f "delims=" %%a in ('adb shell getprop ro.product.system.manufacturer') do set "manufactura=%%a"
		call :c 0E " MARCA			: "&call :c 06 "%manufactura%"
		echo.
		call :c 0E " MODELO			: "&call :c 06 "%modelo%"		
		echo.
		call :c 0E " SERIAL NUMBER		: "&call :c 06 "%sn%"
		echo.
		call :c 0E " CHIP			: "&call :c 06 "%chip%"
		echo.
		call :c 0E " IMEI			: "&call :c 06 "%imei%"
		echo.
		call :c 0E " IP PUBLICA		: "&call :c 06 "%ippublica%"
		echo.
		call :c 0E " VERSION ANDROID	: "&call :c 06 "%version%"
		echo.
		call :c 0E " COMPILACION		: "&call :c 06 "%build%"
		echo.
		call :c 0E " VERSION MODEM		: "&call :c 06 "%modem%"
		echo.
		call :c 0E " CODIGO CSC ROM		: "&call :c 06 "%csc%"
		echo.
		call :c 0E " CARRIER_ID		: "&call :c 06 "%carrierid%"
		echo.
		call :c 0E " PARCHE SEGURIDAD	: "&call :c 06 "%security%"
		echo.
		call :c 0E " ESTADO SIM		: "&call :c 06 "%simstate%"
		echo.
		call :c 0E " KG STATUS		: "&call :c 06 "%knox%"
		echo.
		exit/b

:adbreadnc
call :c 0E "  *******************************************************************"
echo.
call :c 0E "  * DISPOSITIVO NO DETECTADO, FAVOR CONECTE O ENTREGUE PERMISOS ADB *"
echo.
call :c 0E "  *******************************************************************"
echo.
echo.
echo.
pause
goto:inicio

:c
setlocal enableDelayedExpansion

:colorPrint Color  Str  [/n]
setlocal
set "s=%~2"
call :colorPrintVar %1 s %3
exit /b

:colorPrintVar  Color  StrVar  [/n]
if not defined DEL call :initColorPrint
setlocal enableDelayedExpansion
pushd .
':
cd \
set "s=!%~2!"
:: The single blank line within the following IN() clause is critical - DO NOT REMOVE
for %%n in (^"^

^") do (
  set "s=!s:\=%%~n\%%~n!"
  set "s=!s:/=%%~n/%%~n!"
  set "s=!s::=%%~n:%%~n!"
)
for /f delims^=^ eol^= %%s in ("!s!") do (
  if "!" equ "" setlocal disableDelayedExpansion
  if %%s==\ (
    findstr /a:%~1 "." "\'" nul
    <nul set /p "=%DEL%%DEL%%DEL%"
  ) else if %%s==/ (
    findstr /a:%~1 "." "/.\'" nul
    <nul set /p "=%DEL%%DEL%%DEL%%DEL%%DEL%"
  ) else (
    >colorPrint.txt (echo %%s\..\')
    findstr /a:%~1 /f:colorPrint.txt "."
    <nul set /p "=%DEL%%DEL%%DEL%%DEL%%DEL%%DEL%%DEL%"
  )
)
if /i "%~3"=="/n" echo(
popd
exit /b


:initColorPrint
for /f %%A in ('"prompt $H&for %%B in (1) do rem"') do set "DEL=%%A %%A"
<nul >"%temp%\'" set /p "=."
subst ': "%temp%" >nul
exit /b


:cleanupColorPrint
2>nul del "%temp%\'"
2>nul del "%temp%\colorPrint.txt"
>nul subst ': /d
exit /b

:salir
    @cls&exit