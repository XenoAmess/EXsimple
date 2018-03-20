#!/bin/bash
screen -S exsimple -X quit
cd /
wget -O /tools/python/exsimple.py https://raw.githubusercontent.com/XenoAmess/EXsimple/master/src/exsimple.py
sed -i "s/THIS_IS_DAILYPASTE = False;/THIS_IS_DAILYPASTE = True;/g" /tools/python/exsimple.py
nuitka --standalone  --recurse-all  --python-version=3.5  /tools/python/exsimple.py  --output-dir=/tools/  --remove-output
sudo screen -dmS exsimple sudo /tools/exsimple.dist/exsimple.exe dir=/DailyPaste