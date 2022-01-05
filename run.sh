#!/bin/bash
# Create a new session named "$sessname", and run command
tmux new-session -d -s "main"

while true; do
  tmux send-keys -t "main" "python3 c14garden.py" Enter
  tmux attach -t "main"
  #python3 c14garden.py
  sleep 10
done
exit
