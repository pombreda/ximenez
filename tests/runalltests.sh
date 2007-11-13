#!/bin/bash

##
## Usage: ./runalltests.sh [/path/to/python-binary]
##

## FIXME: a hand-made test runner until 'test.py' works. Should be
## removed, then.

if [ $# -eq 1 ]
then
    PYTHON="$1"
else
    PYTHON="python"
fi

for i in `ls test_*.py`
do
    $PYTHON $i
done