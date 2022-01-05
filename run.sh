#!/bin/bash
while true; do
  tmux new-session -d -s "log"
  tmux send-keys -t "log" "python3 c14garden.py" Enter
  tmux attach -t "log"
  tmux kill-session -t "log"
  #python3 c14garden.py
  sleep 10
done
exit
