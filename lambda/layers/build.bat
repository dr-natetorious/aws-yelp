@REM =================
@REM The root folder in zip must be called "python"
@REM =================

@RMDIR /S /Q photo-deps\*
@SET target=photo-deps\python

@MKDIR %target%
@DEL /Q photo-deps.zip

@CALL pip install --target %target% matplotlib
@CALL pip install --target %target% opencv-python

@PUSHD photo-deps
7z a -tzip ..\photo-deps.zip .
@POPD

aws s3 cp photo-deps.zip s3://nbachmei.personal/artifacts/
