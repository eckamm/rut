set -eux

# Project specific parameters...
PGM="rut"
APK_NAME="R.U.T."    # TODO: get from .android.json
APK_VERSION="0.0.8"  # TODO: get from source
KEYSTORE="/home/eric/keys/rockwellgamestudio.keystore"
KEYALIAS="main"
SCRIPTDIR=$(readlink -fn "$(dirname "$0")")
SRCDIR=$(readlink -fn "$SCRIPTDIR/../src")

# Utility locations...
PYTHON="/cygdrive/c/Python27/python.exe"
PGS4ADIR="/cygdrive/c/pgs4a-0.9.4"
KEYTOOL="/cygdrive/c/Program Files/Java/jre7/bin/keytool.exe"
JARSIGNER="/cygdrive/c/Program Files/Java/jdk1.7.0_10/bin/jarsigner.exe"
ZIPALIGN="/cygdrive/c/pgs4a-0.9.4/android-sdk/tools/zipalign.exe"

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

function sign_apk {
    local unsigned_apk="${APK_NAME}-${APK_VERSION}-release-unsigned.apk"
    local unaligned_apk=$(echo "$unsigned_apk" | sed 's/unsigned/unaligned/')
    local signed_apk=$(echo "$unaligned_apk" | sed 's/unaligned/signed/')

    mkdir -p dist && cd dist
    # Copy local...
    cp "$PGS4ADIR/bin/$unsigned_apk" .
    chmod 644 "$unsigned_apk"
    # Sign...
    "$JARSIGNER" -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore "$(cygpath -w "$KEYSTORE")" "$unsigned_apk" "$KEYALIAS"
    mv "$unsigned_apk" "$unaligned_apk"
    # Verify...
    "$JARSIGNER" -verify -certs "$unaligned_apk"
    # Align...
    if [ -e "$signed_apk" ]; then rm "$signed_apk"; fi
    "$ZIPALIGN" -v 4 "$unaligned_apk" "$signed_apk"
    rm "$unaligned_apk"
    ls -l "$signed_apk"
}

# Copy the source into a temporary build directory.
setup_source
# Configure the pgs4a project.
(cd $PGS4ADIR && "$PYTHON" android.py configure "$PGM")
# Build the APK.
(cd $PGS4ADIR && "$PYTHON" android.py build "$PGM" release)
(cd $PGS4ADIR && ls -l bin)
# Sign the APK.  Output is in ./dist.
sign_apk

exit 0

# (cd $PGS4ADIR && "$PYTHON" android.py build "$PGM" release install)
# (cd $PGS4ADIR && "$PYTHON" android.py build "$PGM" logcat)