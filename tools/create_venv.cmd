@echo off
setlocal enableextensions
set OLDHOME_FOLDER=%~dp0
set INPATH=%~dp1
set INFILE=%~nx1
set INFILEBASE=%~n1

rem ---------------------------------------------------
set _date=%DATE:/=-%
set _time=%TIME::=%
set _time=%_time: =0%
rem ---------------------------------------------------
rem ---------------------------------------------------
set _decades=%_date:~-2%
set _years=%_date:~-4%
set _months=%_date:~3,2%
set _days=%_date:~0,2%
rem ---------------------------------------------------
set _hours=%_time:~0,2%
set _minutes=%_time:~2,2%
set _seconds=%_time:~4,2%
rem ---------------------------------------------------
set TIMEBLOCK=%_years%-%_months%-%_days%_%_hours%-%_minutes%-%_seconds%
Echo ################# Current time is %TIMEBLOCK%
Echo.
Echo.
Echo.
Echo -------------------------------------------- BASIC VENV SETUP --------------------------------------------
Echo.
Echo.
Echo ################# changing directory to %OLDHOME_FOLDER%
cd %OLDHOME_FOLDER%
Echo.
Echo ################# removing old venv folder
RD /S /Q ..\.venv
echo.

Echo ################# creating new venv folder
mkdir ..\.venv
echo.
Echo ################# calling venv module to initialize new venv
python -m venv ..\.venv
echo.

Echo ################# changing directory to ..\.venv
cd ..\.venv
echo.
Echo ################# activating venv for package installation
call .\Scripts\activate.bat
echo.

Echo ################# upgrading pip to get rid of stupid warning
call %OLDHOME_FOLDER%get-pip.py
echo.
echo.
echo.
Echo -------------------------------------------- INSTALLING PACKAGES --------------------------------------------
echo.
echo.
Echo +++++++++++++++++++++++++++++ Standard Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing Setuptools
call pip install setuptools
echo.
Echo ################# Installing pywin32
call pip install pywin32
echo.
Echo ################# Installing python-dotenv
call pip install python-dotenv
echo.
echo.
rem Echo +++++++++++++++++++++++++++++ Qt Packages +++++++++++++++++++++++++++++
rem echo.
rem Echo ################# Installing PyQt5
rem call pip install PyQt5
rem echo.
rem Echo ################# Installing pyopengl
rem call pip install pyopengl
rem echo.
rem Echo ################# Installing PyQt3D
rem call pip install PyQt3D
rem echo.
rem Echo ################# Installing PyQtChart
rem call pip install PyQtChart
rem echo.
rem Echo ################# Installing PyQtDataVisualization
rem call pip install PyQtDataVisualization
rem echo.
rem Echo ################# Installing PyQtWebEngine
rem call pip install PyQtWebEngine
rem echo.
rem Echo ################# Installing pyqtgraph
rem call pip install pyqtgraph
rem echo.
rem Echo ################# Installing QScintilla
rem call pip install QScintilla
rem echo.

echo.

Echo +++++++++++++++++++++++++++++ Packages From Github +++++++++++++++++++++++++++++
echo.
Echo ################# Installing git+https://github.com/overfl0/Armaclass.git
call pip install git+https://github.com/overfl0/Armaclass.git
echo.


echo.

rem Echo +++++++++++++++++++++++++++++ Misc Packages +++++++++++++++++++++++++++++
rem echo.
rem Echo ################# Installing pyperclip
rem call pip install pyperclip
rem echo.
Echo ################# Installing jinja2
call pip install jinja2
echo.
Echo ################# Installing bs4
call pip install bs4
echo.
Echo ################# Installing requests
call pip install requests
echo.
Echo ################# Installing PyGithub
call pip install PyGithub
echo.
Echo ################# Installing fuzzywuzzy
call pip install fuzzywuzzy
echo.
rem Echo ################# Installing fuzzysearch
rem call pip install fuzzysearch
rem echo.
Echo ################# Installing python-Levenshtein
call pip install python-Levenshtein
echo.
Echo ################# Installing jsonpickle
call pip install jsonpickle
echo.
Echo ################# Installing discord.py
call pip install discord.py
echo.
Echo ################# Installing regex
call pip install regex
echo.


echo.
Echo +++++++++++++++++++++++++++++ Gid Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils
call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils
echo.
rem Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidqtutils
rem call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidqtutils
rem echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidlogger_rep
call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidlogger_rep
echo.
rem Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_Vscode_Wrapper
rem call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_Vscode_Wrapper
rem echo.
rem Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_View_models
rem call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_View_models
rem echo.
rem echo.

Echo ################# changing directory to %OLDHOME_FOLDER%
cd %OLDHOME_FOLDER%
echo.
Echo ################# writing ..\requirements_dev.txt
echo ########################################################## created at --^> %TIMEBLOCK% ##########################################################> ..\requirements_dev.txt
call pip freeze >> ..\requirements_dev.txt
echo.
echo.
echo.
Echo +++++++++++++++++++++++++++++ Test Packages +++++++++++++++++++++++++++++
echo.

rem Echo ################# Installing pytest-qt
rem call pip install pytest-qt
rem echo.
Echo ################# Installing pytest
call pip install pytest
echo.

echo.
Echo +++++++++++++++++++++++++++++ Dev Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing wheel
call pip install --no-cache-dir wheel
echo.
rem Echo ################# Installing https://github.com/pyinstaller/pyinstaller/tarball/develop
rem call pip install --force-reinstall --no-cache-dir https://github.com/pyinstaller/pyinstaller/tarball/develop
rem echo.
Echo ################# Installing pep517
call pip install  --no-cache-dir pep517
echo.
rem Echo ################# Installing pyqt5-tools==5.15.1.1.7.5
rem call pip install --pre pyqt5-tools==5.15.1.1.7.5
rem echo.
rem Echo ################# Installing PyQt5-stubs
rem call pip install PyQt5-stubs
rem echo.
rem Echo ################# Installing sip
rem call pip install sip
rem echo.
rem Echo ################# Installing PyQt-builder
rem call pip install PyQt-builder
rem echo.
rem Echo ################# Installing pyqtdeploy
rem call pip install pyqtdeploy
rem echo.
rem Echo ################# Installing nuitka
rem call pip install nuitka
rem echo.
rem Echo ################# Installing memory-profiler
rem call pip install memory-profiler
rem echo.
rem Echo ################# Installing matplotlib
rem call pip install matplotlib
rem echo.
rem Echo ################# Installing import-profiler
rem call pip install import-profiler
rem echo.
rem Echo ################# Installing objectgraph
rem call pip install objectgraph
rem echo.
rem Echo ################# Installing pipreqs
rem call pip install pipreqs
rem echo.
rem Echo ################# Installing pydeps
rem call pip install pydeps
rem echo.
Echo ################# Installing bootstrap-discord-bot
call pip install bootstrap-discord-bot
echo.
rem echo.

rem echo -------------------calling pyqt5toolsinstalluic.exe-----------------------------
rem call ..\.venv\Scripts\pyqt5toolsinstalluic.exe
rem echo.
rem echo.

echo.
Echo ################# converting ..\requirements_dev.txt to ..\requirements.txt by calling %OLDHOME_FOLDER%convert_requirements_dev_to_normal.py
call %OLDHOME_FOLDER%convert_requirements_dev_to_normal.py
echo.
Echo INSTALL THE PACKAGE ITSELF AS -dev PACKAGE SO I DONT HAVE TO DEAL WITH RELATIVE PATHS
rem call pip install -e ..
call pip install --no-cache-dir --force-reinstall -e ..
echo.
echo.
echo ###############################################################################################################
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ---------------------------------------------------------------------------------------------------------------
echo                                                     FINISHED
echo ---------------------------------------------------------------------------------------------------------------
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ###############################################################################################################