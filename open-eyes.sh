#!/bin/bash
# need to set path to get uvcdynctrl to work in the script!
uvcdynctrl -s 'Brightness' 0.1

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo $DIR
#cd ~/.virtualenvs/automator-eyes
source $DIR"/bin/activate"

python $DIR"/server.py" --local --rotate -3 > $DIR/"logs.txt" &
source $DIR"/bin/deactivate"
