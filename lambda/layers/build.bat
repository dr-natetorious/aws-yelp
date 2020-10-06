@RMDIR /S /Y photo-deps\*
@DEL /Y photo-deps.zip

pip install --target photo-deps matplotlib
pip install --target photo-deps opencv-python
@PUSHD photo-deps
7z a -tzip ..\photo-deps.zip .
@POPD

