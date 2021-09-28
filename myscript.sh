#!/usr/bin/env bash

python3 server.py &

while true; do
    python3 discount.py
    sleep 86400
done
