#!/bin/sh

# auto restart the './stream_db.py' if exits with error

until ./stream_db.py; do
    echo "Server crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
