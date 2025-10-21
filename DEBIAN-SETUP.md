# Debian Setup Guide - Dell Chromebook 3120

**Complete setup guide for running Samsung DEX on Debian Linux**

## Your Hardware

- **Computer**: Dell Chromebook 3120 running Debian
- **Phone**: Samsung S24 Ultra
- **Connection**: USB-A to USB-C cable

## Prerequisites Check

First, verify your Debian system:

```bash
# Check Debian version
cat /etc/debian_version

# Should show something like: 12.x (Bookworm) or 11.x (Bullseye)
```

## Installation - Debian Specific

### Method 1: Automated Installation (Recommended)

```bash
cd DEXtrobution
sudo ./install.sh
```

The script will automatically:
- ✅ Detect Debian system
- ✅ Install all dependencies from Debian repos
- ✅ Configure Python libraries
- ✅ Set up USB permissions

### Method 2: Manual Installation (If needed)

If you prefer manual installation or automated script fails:

```bash
# 1. Update Debian package lists
sudo apt update

# 2. Install core dependencies
sudo apt install -y \
    python3 \
    python3-pip \
    android-tools-adb \
    android-tools-fastboot \
    scrcpy \
    ffmpeg \
    libnotify-bin

# 3. Install Python dependencies
sudo pip3 install pexpect netifaces

# 4. Set up USB permissions
sudo tee /etc/udev/rules.d/51-android.rules << 'EOF'
# Samsung devices
SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", MODE="0666", GROUP="plugdev"
EOF

sudo chmod a+r /etc/udev/rules.d/51-android.rules
sudo udevadm control --reload-rules

# 5. Add yourself to plugdev group
sudo usermod -aG plugdev $USER

# 6. Make scripts executable
chmod +x dexlauncher.py tuxdex.py test-cable.sh
```

**Important**: Log out and log back in after installation for group changes to take effect!

## Debian-Specific Package Notes

### Debian 12 (Bookworm) - Latest Stable

✅ **Everything available in default repos**
```bash
sudo apt install adb scrcpy python3-pip
```

### Debian 11 (Bullseye) - Older Stable

⚠️ **scrcpy might need backports**
```bash
# If scrcpy not found in main repos:
sudo sh -c 'echo "deb http://deb.debian.org/debian bullseye-backports main" >> /etc/apt/sources.list'
sudo apt update
sudo apt install -y scrcpy/bullseye-backports
```

### Debian 10 (Buster) - Old Stable

⚠️ **May need manual scrcpy installation**
```bash
# Install via snap if available:
sudo apt install snapd
sudo snap install scrcpy

# OR download from GitHub releases
```

## Dell Chromebook 3120 Specific Tips

### Performance Optimization for Older Hardware

Your Dell 3120 specs (typical):
- CPU: Intel Celeron N2840 (Bay Trail)
- RAM: 2GB or 4GB
- GPU: Intel HD Graphics

**Recommended settings for smooth performance:**

```bash
# Launch with lower resolution and bitrate
scrcpy --new-display=1280x720 --bit-rate=2M --max-fps=30
```

### Check Your Debian Installation

```bash
# Verify you're running Debian (not ChromeOS)
uname -a
cat /etc/os-release

# Should show: ID=debian
```

### If You Dual-Boot or Have ChromeOS

Some Dell Chromebooks run:
1. **ChromeOS only** - You'll need to enable Linux (Crostini) or install full Debian
2. **Dual-boot** - Boot into Debian for DEX
3. **Full Debian replacement** - You're all set!

## Networking on Debian

### For Wireless ADB Connection

Make sure NetworkManager is running (default on Debian):

```bash
# Check NetworkManager status
systemctl status NetworkManager

# Should be: active (running)
```

### WiFi Direct Support (for TuxDex/Miraclecast)

Check if your WiFi adapter supports P2P:

```bash
# Install iw tool if not present
sudo apt install iw

# Check for P2P support
iw list | grep -A 10 "Supported interface modes" | grep P2P
```

If you see "P2P-client" and "P2P-GO", your adapter supports WiFi Direct!

## Step-by-Step First Connection

### 1. Prepare Your Phone

On your S24 Ultra:
```
Settings → About Phone → Software Information
→ Tap "Build Number" 7 times

Settings → Developer Options
→ Enable "USB Debugging"
→ Enable "Wireless Debugging" (optional)
```

### 2. Connect USB Cable

- Plug USB-A side into Dell 3120
- Plug USB-C side into S24 Ultra
- Phone shows "Allow USB debugging?" → Tap OK
- Check "Always allow from this computer"

### 3. Test Connection

```bash
cd DEXtrobution

# Test cable and connection
./test-cable.sh

# Should show: ✅ SUCCESS! Your cable works perfectly!
```

### 4. Launch DEX

```bash
# Start the launcher
./dexlauncher.py

# Choose option 1 (USB Connection)
# DEX window appears!
```

## Troubleshooting - Debian Specific

### Issue: "adb: command not found"

**Fix:**
```bash
sudo apt install android-tools-adb android-tools-fastboot
```

### Issue: "scrcpy: command not found"

**Fix for Debian 12:**
```bash
sudo apt install scrcpy
```

**Fix for Debian 11:**
```bash
# Enable backports
echo "deb http://deb.debian.org/debian bullseye-backports main" | sudo tee -a /etc/apt/sources.list
sudo apt update
sudo apt install -y scrcpy/bullseye-backports
```

**Fix for older Debian:**
```bash
# Use snap
sudo apt install snapd
sudo snap install scrcpy
```

### Issue: "Permission denied" when running adb

**Fix:**
```bash
# Add yourself to plugdev group
sudo usermod -aG plugdev $USER

# Reload udev rules
sudo udevadm control --reload-rules

# Log out and log back in
# Then reconnect phone
```

### Issue: Low performance on Dell 3120

**Fix - Use lower settings:**
```bash
# Edit dexlauncher.py
nano dexlauncher.py

# Find line ~147, change resolution:
resolution: str = "1280x720"  # Instead of 1920x1080

# Or launch manually with optimized settings:
scrcpy --new-display=1024x768 --bit-rate=1.5M --max-fps=24
```

### Issue: WiFi stops working after using TuxDex

**Fix:**
```bash
# Restore NetworkManager
sudo ./tuxdex-restore.sh

# Or manually:
sudo systemctl restart NetworkManager wpa_supplicant
```

## Debian Desktop Environments

DEXtrobution works with all Debian desktop environments:

| Desktop | Tested | Performance | Notes |
|---------|--------|-------------|-------|
| GNOME | ✅ Yes | Good | Default on many Debian systems |
| KDE Plasma | ✅ Yes | Good | May use more RAM |
| XFCE | ✅ Yes | **Best** | Lightweight, great for Dell 3120 |
| LXDE | ✅ Yes | **Best** | Very lightweight |
| MATE | ✅ Yes | Good | Good balance |
| Cinnamon | ✅ Yes | Good | Slightly heavier |

**Recommendation for Dell 3120**: XFCE or LXDE for best performance!

## Checking Your Installation

Run this complete check:

```bash
# Check Debian version
cat /etc/debian_version

# Check required tools
which python3    # Should show: /usr/bin/python3
which adb        # Should show: /usr/bin/adb
which scrcpy     # Should show: /usr/bin/scrcpy or /snap/bin/scrcpy

# Check group membership
groups | grep plugdev  # Should include plugdev

# Check Python libraries
python3 -c "import pexpect; import netifaces; print('✓ Python libs OK')"

# If all pass, you're ready!
```

## Quick Reference - Common Commands

```bash
# Test USB cable
./test-cable.sh

# Launch DEX (recommended method)
./dexlauncher.py

# Launch TuxDex (Miraclecast method)
python3 tuxdex.py

# Check ADB devices
adb devices

# Enable wireless ADB manually
adb tcpip 5555
adb connect <phone-ip>:5555

# Restore networking after TuxDex
sudo ./tuxdex-restore.sh

# Kill scrcpy if stuck
pkill scrcpy

# Restart ADB server
adb kill-server
adb start-server
```

## Performance Tips for Debian on Dell 3120

### 1. Close Unnecessary Programs

```bash
# Before launching DEX, close heavy programs:
# - Web browsers (or close extra tabs)
# - Office applications
# - Video players

# Check memory usage
free -h
```

### 2. Use Lightweight Desktop

```bash
# If using GNOME and it's slow, consider XFCE:
sudo apt install xfce4
# Then log out and select XFCE session
```

### 3. Disable Visual Effects

```bash
# In GNOME: Settings → Accessibility → Turn on "Reduce Animation"
# In KDE: System Settings → Workspace Behavior → Desktop Effects → Disable
```

### 4. Optimize scrcpy Settings

Create a launcher script with optimized settings:

```bash
nano ~/launch-dex-optimized.sh
```

Add:
```bash
#!/bin/bash
scrcpy --new-display=1280x720 \
       --bit-rate=2M \
       --max-fps=30 \
       --stay-awake \
       --display-buffer=30
```

Save and make executable:
```bash
chmod +x ~/launch-dex-optimized.sh
./launch-dex-optimized.sh
```

## Next Steps

1. ✅ Run installation: `sudo ./install.sh`
2. ✅ Test cable: `./test-cable.sh`
3. ✅ Launch DEX: `./dexlauncher.py`
4. ✅ Enjoy your S24 Ultra as a desktop!

## Getting Help

- **Full documentation**: See [README.md](README.md)
- **Quick start**: See [QUICKSTART.md](QUICKSTART.md)
- **Issues**: https://github.com/helixexpress9119-max/DEXtrobution/issues

## Debian Resources

- Debian Wiki: https://wiki.debian.org
- Debian Forums: https://forums.debian.net
- Android Tools in Debian: https://packages.debian.org/search?keywords=android-tools

---

**Optimized for Debian Linux on Dell Chromebook 3120**

*Your S24 Ultra + Dell 3120 = Perfect DEX Workstation!*
