pyinstaller -y ^
--onefile ^
--noconsole ^
--icon=modules\ico\app.ico ^
--add-data "modules/ico";"modules/ico" ^
ThumbnailsGUI.pyw
pause