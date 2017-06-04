#!/bin/bash

uvcdynctrl -s 'Brightness' 0.1
cd ~/.virtualenvs/automator-eyes
source bin/activate

python main.py --local --rotate -3 > logs.txt &
source bin/deactivate
