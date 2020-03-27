@echo off
set "CURRENT_DIR=%cd%"
echo PATH "%EXECUTABLE%"
rem cd ../..
rem CATALINA_HOME为python的工作路径
set "CATALINA_HOME=C:\Python27\Lib\site-packages"
rem COPY D:\work\python\AppAuto\src\src\runner\runner.py D:\work\python\AAA
if not exist %CATALINA_HOME%\autoFilmora (md %CATALINA_HOME%\autoFilmora)
if exist %cd%\autoFilmora\ (
Xcopy %cd%\autoFilmora %CATALINA_HOME%\autoFilmora  /s /e /y)
cd autoFilmora\src
python main.py
)
pause