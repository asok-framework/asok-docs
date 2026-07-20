@ECHO OFF

pushd %~dp0

REM Command line options.
IF "%SPHINXBUILD%" == "" (
	SET SPHINXBUILD=sphinx-build
)
SET SOURCEDIR=.
SET BUILDDIR=_build

%SPHINXBUILD% >NUL 2>NUL
IF ERRORLEVEL 9009 (
	ECHO.
	ECHO.The 'sphinx-build' command was not found. Make sure you have Sphinx
	ECHO.installed, then add the directory containing it to your PATH.
	ECHO.
	ECHO.If you don't have Sphinx installed, grab it from
	ECHO.https://www.sphinx-doc.org/
	EXIT /B 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
GOTO end

:end
popd
