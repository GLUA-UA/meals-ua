sudo pip3 install xmltodict # Install dependency
CAMINHO=$(pwd)              # Get current path
# Check if alias already exists
if ! grep -q "alias ementa=" ~/.bashrc; then
    # Create alias
    sudo echo "alias ementa=\"python3 $CAMINHO/ementas@ua.py\"" >> ~/.bashrc
fi
if ! grep -q "alias ementa=" ~/.zshrc; then
    sudo echo "alias ementa=\"python3 $CAMINHO/ementas@ua.py\"" >> ~/.zshrc
fi