#!/usr/bin/env sh

if [ "$1" = "-v" ]; then
  set -x
fi

## Install Python dependencies
pip3 install --user -r requirements.txt # Install dependencies

## Default install path in systemd file-hierarchy spec
INSTALL_DIR="$HOME/.local/bin"

mkdir -p $INSTALL_DIR

ln -s $(pwd)/meals-ua.py ${INSTALL_DIR}/ementas
