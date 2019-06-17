#!/usr/bin/env sh

## print commands (debug mode)
[ "$1" = "-v" ] && set -x

## Default install path in systemd file-hierarchy spec
INSTALL_DIR="$HOME/.local/bin"

## check and create directory
mkdir -p $INSTALL_DIR

## Verify if PATH contains $HOME/.local/bin and add it if not
if [[ ${PATH} != *"${HOME}/.local/bin"* ]]; then
	touch $HOME/.pam_environment
	echo "PATH DEFAULT=\${PATH}:/home/@{PAM_USER}/.local/bin" >> $HOME/.pam_environment
  echo "Relog and the rerun ./install.sh"
else
  ## Install Python dependencies
  pip3 install --user -r requirements.txt # Install dependencies
    
  chmod +x meals-ua.py
  
  ## Verify if is already exists and removes if true.
  [ -f ${INSTALL_DIR}/ementas ] && rm -f ${INSTALL_DIR}/ementas 

  cp $(pwd)/meals-ua.py ${INSTALL_DIR}/ementas 

fi
