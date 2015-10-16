#!/bin/bash
mkdir build
cp handler.py build/
cp util.py build/
cp customresource.py build/
pip install -r requirements.txt -t ./build
cd build
zip -X -r ../handler.zip ./
cd ..
rm -rf build
