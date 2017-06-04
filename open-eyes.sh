#!/bin/bash

uvcdynctrl -s 'Brightness' 0.1

workon automator-eyes
python /opt/automator-eyes/main.py --local --rotate -3 > logs.txt &
