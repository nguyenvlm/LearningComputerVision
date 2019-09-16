if not exist ".\lib" mkdir lib;

call pyuic5 -o .\lib\gui.py .\resource\xml\mainwindow.ui --resource-suffix=""
call pyrcc5 -o .\darkmode.py .\resource\darkmode.qrc