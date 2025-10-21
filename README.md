# DEXtrobution

**Samsung DEX Integration for Linux** - Run Samsung DEX on your Linux machine with your S24 Ultra and other Samsung devices.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)

## Overview

DEXtrobution provides two methods to run Samsung DEX on Linux:

1. **Enhanced DEX Launcher** (Recommended for S24 Ultra and newer devices) - Uses virtual display mode with scrcpy
2. **TuxDex** (Original method) - Uses Miraclecast for wireless display mirroring

## Features

### Enhanced DEX Launcher (New!)

- ✨ Virtual display mode for One UI 8+ devices (S24 Ultra compatible)
- 🔌 USB and wireless (TCP/IP) connection support
- 🎯 Simple, user-friendly interface with color-coded menus
- ⚡ Fast setup with automated wireless ADB configuration
- 🖥️ Customizable resolution support
- 🛡️ No need to disable NetworkManager

### TuxDex (Classic)

- 📡 Wireless display mirroring via Miraclecast
- 🎵 Audio streaming support via RTP
- 🔄 Display 2 support for DEX desktop mode
- 💪 Battle-tested on multiple devices

## Compatibility

### Tested Devices
- **Phone**: Samsung Galaxy S24 Ultra (One UI 8+)
- **Computer**: Dell Chromebook 3120 running Debian Linux
- **Also compatible**: S23, S22, S21, S20 series and other Samsung devices with DEX support

### Requirements

- **OS**: Debian-based Linux (Debian, Ubuntu, Linux Mint, etc.)
- **Python**: 3.6 or higher
- **Phone**: Samsung device with DEX support
- **USB Cable**: For initial setup or wired connection

## Installation

### Quick Install

```bash
git clone https://github.com/helixexpress9119-max/DEXtrobution.git
cd DEXtrobution
sudo ./install.sh
```

The installation script will:
- Install all required dependencies (adb, scrcpy, ffmpeg, etc.)
- Set up Python libraries (pexpect, netifaces)
- Configure udev rules for Android devices
- Optionally install Miraclecast for wireless display
- Create desktop shortcuts

### Manual Installation

If you prefer to install manually:

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip adb scrcpy ffmpeg libnotify-bin

# Install Python dependencies
sudo pip3 install -r requirements.txt

# Make scripts executable
chmod +x dexlauncher.py tuxdex.py
```

## Phone Setup

### Enable USB Debugging

1. Go to **Settings** > **About Phone** > **Software Information**
2. Tap **Build Number** 7 times to enable Developer Options
3. Go to **Settings** > **Developer Options**
4. Enable **USB Debugging**
5. Enable **Wireless Debugging** (optional, for wireless connection)

### First Connection

1. Connect your Samsung S24 Ultra to your computer via USB
2. A popup will appear on your phone asking to "Allow USB debugging"
3. Check "Always allow from this computer" and tap **OK**

## Usage

### Method 1: Enhanced DEX Launcher (Recommended)

```bash
./dexlauncher.py
```

**Connection Options:**

1. **USB Connection** - Connect via USB cable (fastest, most reliable)
2. **Wireless Connection** - Connect via TCP/IP (requires IP address)
3. **Setup Wireless ADB** - Configure wireless ADB via USB first, then go wireless
4. **Miraclecast Mode** - Launch the classic TuxDex method

**Example Workflow:**

```bash
# First time setup - establish wireless connection
./dexlauncher.py
# Select option 3 (Setup Wireless ADB)
# After setup, you can unplug USB and use wireless mode

# Future sessions - connect wirelessly
./dexlauncher.py
# Select option 2 (Wireless Connection)
# Enter your phone's IP address
```

#### Getting Your Phone's IP Address

**Option 1 - Automatic (via launcher):**
- Use option 3 "Setup Wireless ADB" in the launcher

**Option 2 - Manual:**
1. On your phone: Settings > Connections > Wi-Fi
2. Tap on your connected network
3. Find the IP address (e.g., 192.168.1.100)

### Method 2: TuxDex (Classic Miraclecast Method)

```bash
python3 tuxdex.py
```

**Note:** This method temporarily disables NetworkManager and requires Miraclecast to be installed.

**Steps:**
1. Select your Wi-Fi Direct capable interface
2. Enter sudo password to start Miraclecast
3. On your phone: Open DEX and connect to the wireless display
4. Choose connection type (USB or TCP)

## Advanced Configuration

### Custom Resolution for Virtual Display

Edit `dexlauncher.py` or pass resolution when prompted:

```python
# Common resolutions:
# 1920x1080 (Full HD) - Default
# 2560x1440 (QHD)
# 3840x2160 (4K) - May impact performance
```

### Wireless ADB Port Configuration

Default port is 5555. To change:

```bash
adb tcpip <port_number>
```

### Audio Configuration (TuxDex)

Audio is streamed via RTP on port 1991. You can adjust audio quality in `tuxdex.py`:

```python
# Lower quality (less bandwidth):
-ar 22050 -ac 1 -b:a 512k

# Higher quality (more bandwidth):
-ar 48000 -ac 2 -b:a 320k
```

## Troubleshooting

### Device Not Found

**Problem**: ADB cannot find your device

**Solutions:**
1. Ensure USB Debugging is enabled
2. Try a different USB cable (must be data cable, not charge-only)
3. Unplug and replug the USB cable
4. On your phone, revoke USB debugging authorizations and try again:
   Settings > Developer Options > Revoke USB Debugging Authorizations

### Wireless Connection Fails

**Problem**: Cannot connect via TCP/IP

**Solutions:**
1. Ensure phone and computer are on the same Wi-Fi network
2. Check your phone's IP address is correct
3. Verify wireless ADB is enabled: `adb devices` should show IP:port
4. Try disabling and re-enabling wireless debugging on your phone
5. Check firewall settings on your computer

### Black Screen in DEX

**Problem**: DEX launches but shows black screen

**Solutions:**
1. Ensure you have One UI 8+ for virtual display mode
2. Try USB connection first before wireless
3. Reduce display resolution
4. Update scrcpy: `sudo apt update && sudo apt install scrcpy`

### Miraclecast Connection Issues (TuxDex)

**Problem**: Cannot connect via Miraclecast

**Solutions:**
1. Ensure your Wi-Fi adapter supports P2P mode:
   ```bash
   iw list | grep "P2P"
   ```
2. Disable NetworkManager manually if auto-disable fails:
   ```bash
   sudo systemctl stop NetworkManager wpa_supplicant
   ```
3. Restart Miraclecast services
4. Use the restore script if things get stuck:
   ```bash
   sudo ./tuxdex-restore.sh
   ```

### Permission Denied Errors

**Problem**: Permission errors when running commands

**Solutions:**
1. Ensure you're in the plugdev group: `groups`
2. If not, add yourself: `sudo usermod -aG plugdev $USER`
3. Log out and log back in for group changes to take effect
4. Reload udev rules: `sudo udevadm control --reload-rules`

## Performance Tips

### For Best Performance:

1. **Use USB connection** when possible for lowest latency
2. **Close unnecessary apps** on your phone before starting DEX
3. **Use 1920x1080 resolution** for balanced performance
4. **Ensure stable Wi-Fi** when using wireless mode
5. **Keep phone plugged in** during extended sessions

### For Better Quality:

```bash
# Launch with higher bitrate
scrcpy --new-display=1920x1080 --bit-rate=8M --stay-awake
```

## Project Structure

```
DEXtrobution/
├── dexlauncher.py          # Enhanced DEX launcher (new method)
├── tuxdex.py               # Original TuxDex launcher
├── miracles.py             # Miraclecast integration
├── capabilitiesCheck.py    # System capability checking
├── tuxdex-restore.sh       # Restore NetworkManager script
├── install.sh              # Installation script
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── LICENSE                 # License file
```

## Limitations

### Enhanced DEX Launcher
- Requires One UI 8+ for virtual display mode (S24 Ultra has this)
- No audio forwarding in scrcpy (use Bluetooth headphones or speakers)
- Performance depends on USB cable quality and Wi-Fi stability

### TuxDex (Classic)
- Temporarily disables NetworkManager during Miraclecast connection
- Requires P2P-capable Wi-Fi adapter
- More complex setup process
- May not work on all Linux distributions

## FAQ

**Q: Which method should I use?**
A: For S24 Ultra and newer devices, use the Enhanced DEX Launcher (`./dexlauncher.py`). It's simpler and doesn't require disabling NetworkManager.

**Q: Can I use DEX wirelessly?**
A: Yes! Use option 3 in the Enhanced DEX Launcher to set up wireless ADB, then you can use DEX without USB cable.

**Q: Does this work on Ubuntu?**
A: Yes! This works on all Debian-based distributions including Ubuntu, Linux Mint, Pop!_OS, etc.

**Q: Can I use my phone while DEX is running?**
A: Yes, but the DEX virtual display is separate from your phone's main screen. You can interact with both.

**Q: Why is audio not working?**
A: scrcpy doesn't forward audio by default. Use Bluetooth audio devices or the TuxDex method which includes audio streaming.

**Q: Can I use multiple monitors?**
A: The virtual display creates one DEX instance. You can use your Linux desktop on other monitors as normal.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Development Setup

```bash
git clone https://github.com/helixexpress9119-max/DEXtrobution.git
cd DEXtrobution
# Make your changes
# Test thoroughly
# Submit a pull request
```

## Credits

- **Original TuxDex**: Based on the TuxDex project by [semarainc](https://github.com/semarainc/TuxDex)
- **scrcpy**: [Genymobile/scrcpy](https://github.com/Genymobile/scrcpy)
- **Miraclecast**: [albfan/miraclecast](https://github.com/albfan/miraclecast)
- **Enhanced DEX Launcher**: Developed for this project

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [existing issues](https://github.com/helixexpress9119-max/DEXtrobution/issues)
3. Create a new issue with:
   - Your Linux distribution and version
   - Your Samsung phone model
   - Output of `adb devices`
   - Error messages or logs

## Changelog

### v2.0 (Current)
- Added Enhanced DEX Launcher with virtual display support
- Added automated wireless ADB setup
- Added installation script
- Improved documentation
- Added color-coded terminal interface
- Support for S24 Ultra and One UI 8+

### v1.0
- Original TuxDex implementation
- Miraclecast wireless display support
- USB and TCP/IP connection support

---

**Made with ❤️ for the Linux and Samsung DEX community**

*Enjoy your Samsung DEX experience on Linux!*
