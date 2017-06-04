#!/bin/bash

uvcdynctrl -s 'Brightness' 0.1

workon automator-eyes
python ~/.virtualenvs/automator-eyes/main.py --local --rotate -3 > logs.txt &
