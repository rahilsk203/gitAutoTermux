#!/bin/bash

# Auto-Installation Script for gitauto.py (Linux)
echo "=========================================="
echo "🚀 Setting up gitauto.py for Linux..."
echo "=========================================="

# Step 1: Check and Install Python
echo -e "\n🔍 Checking for Python installation..."
if command -v python3 &>/dev/null; then
    echo "✅ Python is already installed."
else
    echo "❌ Python is not installed. Installing Python..."
    sudo apt update && sudo apt install -y python3
    echo "✅ Python installed successfully."
fi

# Step 2: Check and Install Git
echo -e "\n🔍 Checking for Git installation..."
if command -v git &>/dev/null; then
    echo "✅ Git is already installed."
else
    echo "❌ Git is not installed. Installing Git..."
    sudo apt install -y git
    echo "✅ Git installed successfully."
fi

# Step 3: Create the gitAuto directory
GIT_AUTO_DIR="/opt/gitAuto"
echo -e "\n📂 Creating gitAuto directory..."
if [ ! -d "$GIT_AUTO_DIR" ]; then
    sudo mkdir -p "$GIT_AUTO_DIR"
    echo "✅ Directory created: $GIT_AUTO_DIR"
else
    echo "✅ Directory already exists: $GIT_AUTO_DIR"
fi

# Step 4: Copy gitauto.py to /opt/gitAuto/
echo -e "\n📄 Copying gitauto.py to $GIT_AUTO_DIR..."
if [ -f "gitauto.py" ]; then
    sudo cp -f gitauto.py "$GIT_AUTO_DIR/gitauto.py"
    sudo chmod +x "$GIT_AUTO_DIR/gitauto.py"
    echo "✅ gitauto.py copied successfully."
else
    if [ ! -f "$GIT_AUTO_DIR/gitauto.py" ]; then
        echo "❌ gitauto.py not found! Please place it in the current directory."
        exit 1
    else
        echo "✅ gitauto.py already exists in $GIT_AUTO_DIR."
    fi
fi

# Step 5: Ensure gitauto.py has a Python shebang
echo -e "\n🔧 Checking Python shebang in gitauto.py..."
if ! grep -q "^#!/usr/bin/env python3" "$GIT_AUTO_DIR/gitauto.py"; then
    sudo sed -i '1i #!/usr/bin/env python3' "$GIT_AUTO_DIR/gitauto.py"
    echo "✅ Shebang added to gitauto.py."
else
    echo "✅ Shebang already exists in gitauto.py."
fi

# Step 6: Create a wrapper script for the gitauto command
echo -e "\n📝 Creating 'gitauto' command..."
sudo bash -c 'echo "#!/bin/bash
python3 /opt/gitAuto/gitauto.py \""" > /usr/local/bin/gitauto'

# Give execution permission
sudo chmod +x /usr/local/bin/gitauto
echo "✅ 'gitauto' command is now globally available!"

# Step 7: Verify Installation
echo -e "\n🔍 Verifying gitauto command..."
if command -v gitauto &>/dev/null; then
    echo "✅ gitauto command is now available globally!"
else
    echo "❌ Command not found. Please restart your terminal and try again."
    exit 1
fi

# Step 8: Final message
echo -e "\n=========================================="
echo "🎉 Setup completed successfully!"
echo "You can now run 'gitauto' from anywhere."
echo "=========================================="
