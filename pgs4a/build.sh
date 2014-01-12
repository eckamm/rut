set -eux

# Project specific parameters...
PGM="rut"
APK_NAME="R.U.T."    # TODO: get from .android.json
APK_VERSION="0.1.2"  # TODO: get from source
SCRIPTDIR=$(readlink -fn "$(dirname "$0")")
SRCDIR=$(readlink -fn "$SCRIPTDIR/../src")

# Utility locations...
. ~/.utility-config.sh
# Example utility-config.sh:
#     PYTHON="/cygdrive/c/Python27/python.exe"
#     PGS4ADIR="/cygdrive/c/pgs4a-0.9.4"

BUILDDIR="$PGS4ADIR/$PGM"

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
    cp "$PGM.android.json" "$BUILDDIR/.android.json"
}

if [ "${1:-nodev}" == "logcat" ]; then
    (cd $PGS4ADIR && "$PYTHON" android.py logcat)
    exit 0
fi

# Copy the source into a temporary build directory.
setup_source
# Configure the pgs4a project.
(cd $PGS4ADIR && "$PYTHON" android.py configure "$PGM")
if [ "${1:-nodev}" == "dev" ]; then
    # Build the APK, install to device, and start logcat.
    (cd $PGS4ADIR && "$PYTHON" android.py build "$PGM" release install)
    ls -l "$PGS4ADIR/bin"
    (cd $PGS4ADIR && "$PYTHON" android.py logcat)
else
    # Build the APK.
    (cd $PGS4ADIR && "$PYTHON" android.py build "$PGM" release)
    ls -l "$PGS4ADIR/bin"
fi

exit 0
