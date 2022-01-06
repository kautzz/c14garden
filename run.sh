#!/bin/bash
cd /home/pi/c14garden/ &&
while true; do
  python3 c14garden.py
  sleep 10
done
exit
