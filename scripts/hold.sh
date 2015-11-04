#!/bin/bash

if [ -e /tmp/hold.jy ]; then
    rm /tmp/hold.jy
    notify-send -t 1000 "Off Hold"
else
    touch /tmp/hold.jy
    notify-send -t 1000 "On Hold"
fi
