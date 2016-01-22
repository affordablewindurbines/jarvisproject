#!/bin/bash
cronfile="/home/pi/jarvis/setup/cron.orig"

if [[ ! -f $cronfile ]]; then
   crontab -l > $cronfile
   echo cron backup made
fi

cronwork="/home/pi/jarvis/setup/cron.tmp"
cp $cronfile $cronwork

cronwork="/home/pi/jarvis/setup/cron.tmp"
cp $cronfile $cronwork

sed -i 's\^@reboot /home/pi/jarvis/boot/boot.sh;\#@reboot /home/pi/jarvis/boot/boot.sh;\g' $cronwork
crontab $cronwork
rm $cronwork

