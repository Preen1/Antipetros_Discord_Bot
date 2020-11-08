@rem taskarg: ${file}
@Echo off
set OLDHOME_FOLDER=%~dp0
pushd %OLDHOME_FOLDER%
call ..\.venv\Scripts\activate

call memory_profiling_time.cmd ..\src\__main__.py
