# Quick Start Guide - DEXtrobution

Get your Samsung S24 Ultra connected to your Dell Chromebook 3120 (Debian Linux) in minutes!

## 5-Minute Setup

### Step 1: Install (First Time Only)

```bash
cd DEXtrobution
sudo ./install.sh
```

**What it does:**
- Installs adb, scrcpy, and other dependencies
- Sets up Python libraries
- Configures USB permissions

### Step 2: Enable USB Debugging on Your Phone

1. Open **Settings** on your S24 Ultra
2. Go to **About Phone** > **Software Information**
3. Tap **Build Number** 7 times (you'll see a message saying "You are now a developer!")
4. Go back to **Settings** > **Developer Options**
5. Toggle on **USB Debugging**

### Step 3: Connect Your Phone

**Option A: USB Connection (Easiest for first time)**

1. Plug your S24 Ultra into your Dell Chromebook with a USB cable
2. On your phone, tap **OK** when asked to allow USB debugging
3. Check "Always allow from this computer"

**Option B: Wireless Connection (After initial USB setup)**

1. First, set up wireless ADB using the launcher (see below)
2. Then you can use DEX without cables!

### Step 4: Launch DEX

```bash
./dexlauncher.py
```

**For USB Connection:**
- Choose option **1** (USB Connection)
- DEX will launch automatically

**For Wireless Setup:**
- Choose option **3** (Setup Wireless ADB)
- Follow the prompts
- Unplug USB when instructed
- Now you can use DEX wirelessly!

## Daily Usage

Once set up, here's your typical workflow:

### USB Mode (Simple)

```bash
cd DEXtrobution
./dexlauncher.py
# Choose option 1
# DEX launches!
```

### Wireless Mode (No cables!)

```bash
cd DEXtrobution
./dexlauncher.py
# Choose option 2
# Enter your phone's IP (e.g., 192.168.1.100)
# DEX launches!
```

## Finding Your Phone's IP Address

### Method 1: Automatic
1. Use option **3** in the launcher
2. The IP will be displayed automatically

### Method 2: Manual
1. On your S24 Ultra: **Settings** > **Connections** > **Wi-Fi**
2. Tap your connected network name
3. Look for **IP address** (e.g., 192.168.1.100)

## Keyboard Shortcuts in DEX

Once DEX is running:

- **Alt + Tab** - Switch between apps
- **Windows Key** - Open app drawer
- **Alt + F4** - Close current app
- **Ctrl + C / Ctrl + V** - Copy and paste
- **F11** - Toggle fullscreen

## Troubleshooting

### Phone Not Detected?

```bash
# Check if ADB sees your phone
adb devices

# If nothing shows:
# 1. Unplug and replug USB cable
# 2. On phone: Settings > Developer Options > Revoke USB Debugging Authorizations
# 3. Try again
```

### Wireless Connection Not Working?

1. Make sure phone and laptop are on the **same Wi-Fi network**
2. Double-check the IP address
3. Try disabling and re-enabling "Wireless Debugging" on your phone

### DEX Window Is Small?

The default resolution is 1920x1080. You can customize this in the launcher or by editing `dexlauncher.py`.

## Tips for Best Experience

1. **Use USB for setup** - It's faster and more reliable for the first connection
2. **Keep phone charged** - DEX can drain battery quickly
3. **Close unused apps** - Better performance on DEX
4. **Use a good USB cable** - Cheap cables can cause connection issues
5. **Stable Wi-Fi** - Essential for wireless mode

## Need Help?

Check the full **[README.md](README.md)** for:
- Advanced configuration
- Detailed troubleshooting
- Performance optimization
- FAQ

## What's Next?

- Set up wireless ADB for cable-free experience
- Try different resolutions for your workflow
- Explore DEX apps and desktop features
- Use your phone as a full Linux workstation!

---

**Enjoy Samsung DEX on your Dell Chromebook 3120!**

**Having issues?** Check [README.md](README.md) or open an issue on GitHub.
