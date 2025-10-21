#!/bin/bash

# Cable Connection Test Script for DEXtrobution
# Tests if your USB-A to USB-C cable supports data transfer

echo "╔════════════════════════════════════════════╗"
echo "║    DEXtrobution Cable Test Script          ║"
echo "╚════════════════════════════════════════════╝"
echo ""

echo "Testing USB cable connection..."
echo ""

# Check if adb is installed
if ! command -v adb &> /dev/null; then
    echo "❌ ADB is not installed!"
    echo "   Run: sudo apt install adb"
    exit 1
fi

echo "✓ ADB is installed"
echo ""

# Check USB devices
echo "Checking USB devices..."
if lsusb | grep -i samsung &> /dev/null; then
    echo "✓ Samsung device detected in USB!"
    echo ""
    lsusb | grep -i samsung
    echo ""
else
    echo "❌ No Samsung device detected in USB"
    echo ""
    echo "Troubleshooting steps:"
    echo "1. Make sure cable is firmly plugged into both devices"
    echo "2. Try a different USB port on your Dell 3120"
    echo "3. Try unplugging and replugging the cable"
    echo "4. Check if phone is charging (shows it's connected)"
    echo ""
    echo "If phone is charging but not showing in lsusb:"
    echo "→ Your cable might be CHARGE-ONLY (won't work for DEX)"
    echo "→ You need a DATA TRANSFER cable"
    echo ""
    exit 1
fi

# Check ADB connection
echo "Checking ADB connection..."
adb kill-server &> /dev/null
sleep 1
adb start-server &> /dev/null
sleep 2

DEVICES=$(adb devices | grep -v "List of devices" | grep -v "^$" | wc -l)

if [ "$DEVICES" -eq 0 ]; then
    echo "❌ ADB cannot communicate with device"
    echo ""
    echo "Possible issues:"
    echo "1. USB Debugging not enabled on phone"
    echo "   Settings > Developer Options > USB Debugging"
    echo ""
    echo "2. Phone not authorized for USB debugging"
    echo "   Check your phone screen for authorization popup"
    echo ""
    echo "3. Cable is charge-only (doesn't support data)"
    echo "   Try a different cable"
    echo ""
    exit 1
fi

echo "✓ ADB can see device!"
echo ""

# Check authorization status
if adb devices | grep "unauthorized" &> /dev/null; then
    echo "⚠️  Device is connected but UNAUTHORIZED"
    echo ""
    echo "ACTION REQUIRED:"
    echo "1. Look at your S24 Ultra screen"
    echo "2. You should see a popup: 'Allow USB debugging?'"
    echo "3. Check 'Always allow from this computer'"
    echo "4. Tap 'OK'"
    echo ""
    echo "Then run this test again."
    exit 1
fi

if adb devices | grep "device$" &> /dev/null; then
    echo "✅ SUCCESS! Your cable works perfectly!"
    echo ""
    echo "Device details:"
    adb devices -l
    echo ""

    # Get phone model
    MODEL=$(adb shell getprop ro.product.model 2>/dev/null | tr -d '\r')
    ANDROID=$(adb shell getprop ro.build.version.release 2>/dev/null | tr -d '\r')

    if [ ! -z "$MODEL" ]; then
        echo "Phone Model: $MODEL"
        echo "Android Version: $ANDROID"
        echo ""
    fi

    # Test transfer speed
    echo "Testing data transfer speed..."
    echo "(This may take a few seconds)"

    START=$(date +%s)
    adb shell "ls -la /sdcard/" > /dev/null 2>&1
    END=$(date +%s)
    DURATION=$((END - START))

    if [ $DURATION -lt 2 ]; then
        echo "✅ Transfer speed: EXCELLENT"
    elif [ $DURATION -lt 5 ]; then
        echo "✓ Transfer speed: GOOD"
    else
        echo "⚠️  Transfer speed: SLOW (cable quality may be poor)"
    fi

    echo ""
    echo "═══════════════════════════════════════════"
    echo "  Your cable is ready for DEXtrobution!"
    echo "═══════════════════════════════════════════"
    echo ""
    echo "You can now run: ./dexlauncher.py"
    echo ""

    exit 0
fi

echo "❌ Unexpected state"
echo "ADB output:"
adb devices
echo ""
echo "Please report this at:"
echo "https://github.com/helixexpress9119-max/DEXtrobution/issues"
