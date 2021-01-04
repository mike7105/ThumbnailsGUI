O:\Progs\Python\ThumbnailsGUI\venv\Scripts\activate
pyinstaller -y ^
--onefile ^
--noconsole ^
--icon=modules\ico\app.ico ^
--add-data "modules/ico";"modules/ico" ^
-n ThumbnailsGUI_v2.0.exe ^
ThumbnailsGUI.pyw
pause