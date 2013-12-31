set -eux

# Project specific parameters...
PGM="rut"
SCRIPTDIR=$(readlink -fn "$(dirname "$0")")
SRCDIR=$(readlink -fn "$SCRIPTDIR/../src")

# Utility locations...
PYTHON="/cygdrive/c/Python27/python.exe"
ISCC="/cygdrive/c/Program Files (x86)/Inno Setup 5/ISCC.exe"

mkdir -p build
BUILDDIR="build/$PGM"

function setup_source {
    if [ -e "$BUILDDIR" ]; then 
        mv "$BUILDDIR" "$BUILDDIR-junk$$" && rm -rf "$BUILDDIR-junk$$"
    fi
    cp -pr "$SRCDIR" "$BUILDDIR"
    rm -rf "$BUILDDIR/image-dev"
    rm -rf "$BUILDDIR/image-bak"
    rm -rf "$BUILDDIR/imageset-a"
    rm -rf "$BUILDDIR/imageset-c"
    rm -f "$BUILDDIR"/*.pyc
    rm -f "$BUILDDIR"/*.bak
    # TODO: put the version in automatically
    cp py2exe-setup.py "$BUILDDIR/."
}


# Copy the source into a temporary build directory, ./build/$PGM.
setup_source
# Build as a Windows executable.  The py2exe output is in ./build/$PGM/dist.
(cd "$BUILDDIR" && "$PYTHON" py2exe-setup.py) 
# Make a Windows installer.  Output is in ./dist.
"$ISCC" /cc "$PGM.iss" 




