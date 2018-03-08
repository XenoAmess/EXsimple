#!/bin/bash
cd /
wget -O /tools/python/exsimple.py https://raw.githubusercontent.com/XenoAmess/EXsimple/master/src/exsimple.py
sed -i "s/THIS_IS_DAILYPASTE = False;/THIS_IS_DAILYPASTE = True;/g" /tools/python/exsimple.py
sudo screen -dmS exsimple sudo pypy3 /tools/python/exsimple.py dir=/DailyPaste gzip