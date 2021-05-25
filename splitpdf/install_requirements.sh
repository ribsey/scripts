#!/bin/bash

pip=$(command -v pip)
echo $pip
if [ "$pip" = "" ]
then
  pip=$(command -v pip3)
  if [ "$pip" = "" ]
  then
    echo "please install pip first (normally delivered with python)"
    exit 1
  fi
fi

$pip install -r $(dirname $0)/requirements.txt