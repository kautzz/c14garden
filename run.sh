#!/bin/bash
tmux new-session -d -s "log"
#tmux send-keys -t "log" "python3 c14garden.py" Enter

while true; do
  tmux attach -t "log"
  python3 c14garden.py
  tmux kill-session -t "log"

  sleep 10
done
exit
