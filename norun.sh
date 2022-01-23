#!/bin/bash
cd /home/pi/c14garden/ &&
while true; do
  python3 /home/pi/c14garden/c14garden.py
  sleep 10
done
exit
