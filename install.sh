#!/bin/bash

# DEXtrobution Installation Script for Debian Linux
# Optimized for Dell Chromebook 3120 with Samsung S24 Ultra

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════╗"
echo "║    DEXtrobution Installation Script        ║"
echo "║      For Debian Linux Systems              ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running on Debian-based system
if ! [ -f /etc/debian_version ]; then
    echo -e "${RED}Error: This script is designed for Debian-based systems${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Running on Debian-based system${NC}"

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}This script requires sudo privileges${NC}"
    echo "Please run with: sudo ./install.sh"
    exit 1
fi

echo -e "${GREEN}✓ Running with sudo privileges${NC}"
echo ""

# Update package lists
echo -e "${BLUE}Updating package lists...${NC}"
apt update

# Install basic dependencies
echo -e "${BLUE}Installing basic dependencies...${NC}"
apt install -y \
    python3 \
    python3-pip \
    adb \
    ffmpeg \
    libnotify-bin \
    git \
    wget \
    build-essential \
    pkg-config

echo -e "${GREEN}✓ Basic dependencies installed${NC}"

# Install scrcpy
echo -e "${BLUE}Installing scrcpy...${NC}"
if ! command -v scrcpy &> /dev/null; then
    # Check if we can install from apt
    if apt-cache show scrcpy &> /dev/null; then
        apt install -y scrcpy
    else
        echo -e "${YELLOW}scrcpy not in apt, installing from snap...${NC}"
        if command -v snap &> /dev/null; then
            snap install scrcpy
        else
            echo -e "${YELLOW}Installing snapd...${NC}"
            apt install -y snapd
            snap install scrcpy
        fi
    fi
    echo -e "${GREEN}✓ scrcpy installed${NC}"
else
    echo -e "${GREEN}✓ scrcpy already installed${NC}"
fi

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip3 install -r requirements.txt

echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Optional: Install Miraclecast for wireless display
echo ""
echo -e "${YELLOW}Do you want to install Miraclecast for wireless display support?${NC}"
echo "This is optional and requires additional setup."
echo "It's needed for the original TuxDex wireless display method."
read -p "Install Miraclecast? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Installing Miraclecast dependencies...${NC}"
    apt install -y \
        cmake \
        libsystemd-dev \
        libglib2.0-dev \
        libreadline-dev \
        libudev-dev

    if [ ! -d "/tmp/miraclecast" ]; then
        echo -e "${BLUE}Cloning Miraclecast repository...${NC}"
        cd /tmp
        git clone https://github.com/albfan/miraclecast.git
        cd miraclecast
    else
        cd /tmp/miraclecast
    fi

    echo -e "${BLUE}Building Miraclecast...${NC}"
    mkdir -p build
    cd build
    cmake ..
    make
    make install

    echo -e "${GREEN}✓ Miraclecast installed${NC}"
else
    echo -e "${YELLOW}Skipping Miraclecast installation${NC}"
fi

# Set up udev rules for ADB
echo -e "${BLUE}Setting up udev rules for Android devices...${NC}"
cat > /etc/udev/rules.d/51-android.rules << 'EOF'
# Samsung devices
SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", MODE="0666", GROUP="plugdev"

# Generic Android devices
SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666", GROUP="plugdev"
EOF

chmod a+r /etc/udev/rules.d/51-android.rules
udevadm control --reload-rules

echo -e "${GREEN}✓ Udev rules configured${NC}"

# Add user to plugdev group
SUDO_USER_NAME="${SUDO_USER:-$USER}"
if ! groups "$SUDO_USER_NAME" | grep -q plugdev; then
    echo -e "${BLUE}Adding $SUDO_USER_NAME to plugdev group...${NC}"
    usermod -aG plugdev "$SUDO_USER_NAME"
    echo -e "${YELLOW}Note: You may need to log out and back in for group changes to take effect${NC}"
fi

# Make scripts executable
echo -e "${BLUE}Making scripts executable...${NC}"
chmod +x dexlauncher.py
chmod +x tuxdex.py
chmod +x tuxdex-restore.sh

# Create desktop shortcut (optional)
echo ""
echo -e "${YELLOW}Would you like to create a desktop shortcut?${NC}"
read -p "Create shortcut? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    DESKTOP_FILE="/usr/share/applications/dexlauncher.desktop"
    CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=DEXtrobution
Comment=Samsung DEX Launcher for Linux
Exec=$CURRENT_DIR/dexlauncher.py
Icon=phone
Terminal=true
Categories=System;Utility;
Keywords=samsung;dex;android;
EOF

    chmod +x "$DESKTOP_FILE"
    echo -e "${GREEN}✓ Desktop shortcut created${NC}"
fi

# Final setup
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Installation completed successfully!   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "1. Enable USB Debugging on your Samsung S24 Ultra:"
echo "   - Go to Settings > About Phone > Software Information"
echo "   - Tap 'Build Number' 7 times to enable Developer Options"
echo "   - Go to Settings > Developer Options"
echo "   - Enable 'USB Debugging'"
echo ""
echo "2. Connect your S24 Ultra via USB cable"
echo ""
echo "3. Run the launcher:"
echo "   ${GREEN}./dexlauncher.py${NC}"
echo ""
echo "   Or use the classic TuxDex (for Miraclecast):"
echo "   ${GREEN}python3 tuxdex.py${NC}"
echo ""
echo -e "${YELLOW}Note: If you were added to the plugdev group, you may need to log out and back in.${NC}"
echo ""
