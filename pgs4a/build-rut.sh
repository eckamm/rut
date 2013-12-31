
function copy_source {
    set -x
    set +e
    mv rut junk && rm -rf junk
    set -e
    cp -pr /cygdrive/c/Users/Eric.Kamm/Documents/GitHub/rut .
    set +e
    rm -rf rut/screenshots
    rm -rf rut/test
    rm -rf rut/image-dev
    rm -rf rut/image-bak
    rm -rf rut/imageset-a
    rm -rf rut/imageset-c
    rm -f rut/savegame.json
    rm -f rut/*.pyc
    rm -f rut/*.bak
    cp rut.android.json rut/.android.json
    set +x
}

copy_source

/cygdrive/c/Python27/python.exe android.py configure rut

/cygdrive/c/Python27/python.exe android.py build rut release

ls -l bin

#/cygdrive/c/Python27/python.exe android.py build rut release install


#./android.py build worm logcat
