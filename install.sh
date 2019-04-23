CAMINHO=$(pwd)              # Get current path
BASHRC="$HOME/.bashrc"
ZSHRC="$HOME/.zshrc"
COMMAND="\"python3 $CAMINHO/meals-ua.py\""

sudo pip3 install -r $CAMINHO/requirements.txt # Install dependencies

# Check if alias already exists

# Check Configuration file
# Either bashrc or zshrc
if [ -f "$BASHRC" ]; then
    echo "bashrc found"

    if ! grep -q "^alias ementa=" "$BASHRC"; then
        # Create alias
        printf "\n## Ementa UA Script ##\nalias ementa=$COMMAND" >> $BASHRC
    fi
fi
if [ -f "$ZSHRC" ]; then
    echo "zshrc found"

    if ! grep -q "^alias ementa=" ~/.zshrc; then
        # Create alias
        printf "\n## Ementa UA Script ##\nalias ementa=$COMMAND" >> $ZSHRC
    fi
fi
