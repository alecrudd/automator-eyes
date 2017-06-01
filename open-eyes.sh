#!/bin/bash

uvcdynctrl -s 'Brightness' 0.1

cd /opt/automator-eyes/
python main.py
