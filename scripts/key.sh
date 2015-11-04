#!/bin/bash

id="ID 058f:6366 Alcor Micro Corp. Multi Flash Reader"

if [ ! -e /tmp/hold.jy ]; then
    x="$(gdbus call -e -d com.canonical.Unity -o /com/canonical/Unity/Session -m com.canonical.Unity.Session.IsLocked)"
    [ $x == "(false,)" ]; isUnlocked=$?
    [[ -e /tmp/lock.jy || -e /tmp/unlock.jy ]]; isArmed=$?
    [ -n "`lsusb | grep "$id"`" ]; isKeyIn=$?

    if [[ $isArmed == 1 && $isUnlocked == 0 ]]; then                 # unarmed and unlocked
        # echo "unarmed and unlocked"
        if [ $isKeyIn == 0 ]; then                                   # key is in
            # echo "armed now"
            notify-send -t 1000 'Lock Armed'
            touch /tmp/unlock.jy
        fi
    elif [[ $isArmed == 0 && $isUnlocked == 0 ]]; then               # armed and unlocked
        # echo "armed and unlocked"
        if [ $isKeyIn == 1 ]; then                                   # key is not in
            if [ -e /tmp/unlock.jy ]; then
                gnome-screensaver-command -l
                rm /tmp/unlock.jy
                touch /tmp/lock.jy
            else
                # echo "unarmed now"
                notify-send -t 1000 'Lock Unarmed'
                rm /tmp/lock.jy
            fi
        fi
    elif [[ $isArmed == 0 && $isUnlocked == 1 ]]; then               # armed and locked
        # echo "armed and locked"
        if [ $isKeyIn == 0 ]; then                                   # key is in
            # echo "unlocked"
            gnome-screensaver-command -d
            xdotool type dowan; xdotool key Return
            rm /tmp/lock.jy
            touch /tmp/unlock.jy
        fi
    elif [[ $isArmed == 1 && $isUnlocked == 1 ]]; then               # unarmed and locked
        # echo "unarmed and locked"
        if [ $isKeyIn == 0 ]; then                                   # key is in
            # echo "unlocked"
            gnome-screensaver-command -d
            xdotool type dowan; xdotool key Return
        fi
    fi
fi
