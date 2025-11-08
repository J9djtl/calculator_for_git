#!/bin/bash
# Receiving update from server
echo "Receiving update from server..."

git pull

echo "Receiving update successful. Starting building..."
# Building application

mkdir -p calculator-plus/DEBIAN
mkdir -p calculator-plus/usr/bin
mkdir -p calculator-plus/usr/share/calculator-plus
mkdir -p calculator-plus/usr/share/applications

cp main.py frontend.py logic.py memory.py calculator-plus/usr/share/calculator-plus/
cp -r assets calculator-plus/usr/share/calculator-plus/

cat > calculator-plus/DEBIAN/control << EOF
Package: calculator-plus
Version: 1.0.0
Section: utils
Priority: optional
Architecture: all
Depends: python3
Maintainer: Sorokin Svyatoslav Nechaeva Sofya Ermolinskaya Yuliya
Description: Calculator with mathematical functions and memory
EOF

cat > calculator-plus/usr/share/applications/calculator-plus.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Calculator Plus
Comment=Calculator with mathematical functions and memory
Exec=calculator-plus
Icon=/usr/share/calculator-plus/assets/calc.png
Terminal=false
Categories=Utility;
EOF

cat > calculator-plus/usr/bin/calculator-plus << EOF
#!/bin/bash
cd /usr/share/calculator-plus
python3 main.py
EOF
chmod +x calculator-plus/usr/bin/calculator-plus
dpkg-deb --build calculator-plus

echo "Building successful."
# Deleting build directory after building
rm -rf calculator-plus

# Launching unittest
echo "Launching unittest..."
python3 -m unittest

# Installing deb package
echo "Starting installation..."
dpkg -i calculator-plus.deb
