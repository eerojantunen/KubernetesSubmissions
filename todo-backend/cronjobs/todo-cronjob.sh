#!/usr/bin/env bash
set -e

if [ $BACKEND_URL ]
then
  WIKI_REDIRECT=$(curl -sI $WIKI_URL | grep -i "location:" | awk '{print $2}' | tr -d '\r')

  curl -X POST $BACKEND_URL \
    -d "todo=Read $WIKI_REDIRECT"
fi