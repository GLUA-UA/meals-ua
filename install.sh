sudo pip3 install xmltodict # Install dependency

CAMINHO=$(pwd)              # Get current path
BASHRC="$HOME/.bashrc"
ZSHRC="$HOME/.zshrc"

# Check if alias already exists

# Check Configuration file
# Either bashrc or zshrc
if [ -f "$BASHRC" ]; then
    echo "bashrc found"

    if ! grep -q "alias ementa=" "$BASHRC"; then
        # Create alias
        echo "alias ementa=\"python3 $CAMINHO/ementas@ua.py\"" >> ~/.bashrc
    fi
elif [ -f "$ZSHRC" ]; then
    echo "zshrc found"

    if ! grep -q "alias ementa=" ~/.zshrc; then
        echo "alias ementa=\"python3 $CAMINHO/ementas@ua.py\"" >> ~/.zshrc
    fi

fi
