set -eux

# Establish where the tools are...
keytool='/cygdrive/c/Program Files/Java/jre7/bin/keytool.exe'
jarsigner='/cygdrive/c/Program Files/Java/jdk1.7.0_10/bin/jarsigner.exe'
zipalign='/cygdrive/c/pgs4a-0.9.4/android-sdk/tools/zipalign.exe'


# One time - set up a keystore with a key.
#"$keytool" -genkey -v -keystore rockwellgamestudio.keystore -alias main -keyalg RSA  -keysize 2048 -validity 10000


keystore="rockwellgamestudio.keystore"
version="0.0.8"
unsigned_apk="R.U.T.-${version}-release-unsigned.apk"
unaligned_apk=$(echo "$unsigned_apk" | sed 's/unsigned/unaligned/')
signed_apk=$(echo "$unaligned_apk" | sed 's/unaligned/signed/')

cp ../bin/"$unsigned_apk" .
chmod 644 "$unsigned_apk"
"$jarsigner" -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore "$keystore" "$unsigned_apk" main
mv "$unsigned_apk" "$unaligned_apk"

"$jarsigner" -verify -certs "$unaligned_apk"

"$zipalign" -v 4 "$unaligned_apk" "$signed_apk"
