#!/bin/bash

if [ `whoami` != 'root' ]; then
    echo 'This script must be ran as root (sudo!)'
    exit
fi

killall -9 /tmp/payload
killall -9 malware
killall -9 antivirus
