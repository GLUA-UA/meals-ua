#!/usr/bin/env sh

## print commands (debug mode)
if [ "$1" = "-v" ]; then
  set -x
fi

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
	## install python dependencies from remote requirements.txt
	wget -O - https://raw.githubusercontent.com/GLUA-UA/meals-ua/master/requirements.txt | xargs pip3 install --user 

	## get the ementas script and set permissions
	wget https://raw.githubusercontent.com/GLUA-UA/meals-ua/master/meals-ua.py -O $HOME/.local/bin/ementas
	chmod +x $HOME/.local/bin/ementas
fi
