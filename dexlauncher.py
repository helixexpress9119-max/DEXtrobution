#!/usr/bin/env python3
"""
DEXtrobution - Enhanced Samsung DEX Launcher for Linux
Supports S24 Ultra and newer devices with virtual display mode
"""

import os
import sys
import subprocess
import time
import signal
from typing import Optional, Tuple

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DEXLauncher:
    """Main DEX Launcher class"""

    def __init__(self):
        self.adb_process = None
        self.scrcpy_process = None
        self.connected = False

    def print_banner(self):
        """Display application banner"""
        os.system('clear')
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("╔════════════════════════════════════════════╗")
        print("║       DEXtrobution - Samsung DEX           ║")
        print("║         Enhanced Linux Launcher            ║")
        print("╚════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")

    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        dependencies = {
            'adb': 'Android Debug Bridge',
            'scrcpy': 'Screen Copy Tool'
        }

        missing = []
        for cmd, name in dependencies.items():
            if not self.command_exists(cmd):
                missing.append(f"{name} ({cmd})")

        if missing:
            print(f"{Colors.FAIL}Missing dependencies:{Colors.ENDC}")
            for dep in missing:
                print(f"  - {dep}")
            print(f"\n{Colors.WARNING}Please run the installation script first:{Colors.ENDC}")
            print(f"  sudo ./install.sh")
            return False

        print(f"{Colors.OKGREEN}✓ All dependencies installed{Colors.ENDC}")
        return True

    @staticmethod
    def command_exists(command: str) -> bool:
        """Check if a command exists in PATH"""
        try:
            subprocess.run(['which', command],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def get_adb_devices(self) -> list:
        """Get list of connected ADB devices"""
        try:
            result = subprocess.run(['adb', 'devices'],
                                  capture_output=True,
                                  text=True,
                                  check=True)

            devices = []
            for line in result.stdout.split('\n')[1:]:
                if '\tdevice' in line:
                    devices.append(line.split('\t')[0])
            return devices
        except Exception as e:
            print(f"{Colors.FAIL}Error checking ADB devices: {e}{Colors.ENDC}")
            return []

    def connect_adb_usb(self) -> bool:
        """Connect via USB"""
        print(f"\n{Colors.OKCYAN}Checking for USB connected devices...{Colors.ENDC}")

        devices = self.get_adb_devices()

        if not devices:
            print(f"{Colors.WARNING}No devices found via USB.{Colors.ENDC}")
            print("Please ensure:")
            print("  1. USB Debugging is enabled on your phone")
            print("  2. Phone is connected via USB cable")
            print("  3. You've authorized this computer on your phone")
            return False

        print(f"{Colors.OKGREEN}✓ Found device: {devices[0]}{Colors.ENDC}")
        self.connected = True
        return True

    def connect_adb_tcpip(self, ip_address: str, port: int = 5555) -> bool:
        """Connect via TCP/IP (wireless)"""
        print(f"\n{Colors.OKCYAN}Connecting to {ip_address}:{port}...{Colors.ENDC}")

        try:
            # First, check if already connected
            devices = self.get_adb_devices()
            target = f"{ip_address}:{port}"

            if target in devices:
                print(f"{Colors.OKGREEN}✓ Already connected{Colors.ENDC}")
                self.connected = True
                return True

            # Try to connect
            result = subprocess.run(['adb', 'connect', f'{ip_address}:{port}'],
                                  capture_output=True,
                                  text=True,
                                  timeout=10)

            if 'connected' in result.stdout.lower():
                print(f"{Colors.OKGREEN}✓ Connected successfully{Colors.ENDC}")
                self.connected = True
                return True
            else:
                print(f"{Colors.FAIL}Connection failed: {result.stdout}{Colors.ENDC}")
                return False

        except subprocess.TimeoutExpired:
            print(f"{Colors.FAIL}Connection timeout{Colors.ENDC}")
            return False
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
            return False

    def enable_wireless_adb_via_usb(self) -> Optional[str]:
        """Enable wireless ADB via USB connection first"""
        print(f"\n{Colors.OKCYAN}Setting up wireless ADB...{Colors.ENDC}")

        if not self.connect_adb_usb():
            return None

        try:
            # Enable TCP/IP mode on port 5555
            subprocess.run(['adb', 'tcpip', '5555'],
                         check=True,
                         timeout=5)

            time.sleep(2)

            # Get device IP address
            result = subprocess.run(
                ['adb', 'shell', 'ip', 'addr', 'show', 'wlan0'],
                capture_output=True,
                text=True,
                check=True
            )

            # Parse IP address
            for line in result.stdout.split('\n'):
                if 'inet ' in line:
                    ip = line.strip().split()[1].split('/')[0]
                    print(f"{Colors.OKGREEN}✓ Device IP: {ip}{Colors.ENDC}")
                    print(f"{Colors.WARNING}You can now unplug the USB cable{Colors.ENDC}")
                    return ip

            print(f"{Colors.FAIL}Could not determine device IP{Colors.ENDC}")
            return None

        except Exception as e:
            print(f"{Colors.FAIL}Error enabling wireless ADB: {e}{Colors.ENDC}")
            return None

    def launch_dex_virtual_display(self, resolution: str = "1920x1080"):
        """
        Launch DEX using virtual display mode (One UI 8+)
        This is the modern method for S24 Ultra and newer devices
        """
        print(f"\n{Colors.HEADER}Launching Samsung DEX (Virtual Display Mode){Colors.ENDC}")
        print(f"Resolution: {resolution}")
        print(f"\n{Colors.WARNING}Press Ctrl+C to stop DEX{Colors.ENDC}\n")

        try:
            # Build scrcpy command with virtual display
            cmd = [
                'scrcpy',
                f'--new-display={resolution}',
                '--stay-awake',
                '--display-buffer=30',
                '--window-title=Samsung DEX - S24 Ultra',
                '--forward-all-clicks'
            ]

            # Launch scrcpy
            self.scrcpy_process = subprocess.Popen(cmd)

            # Wait for process
            self.scrcpy_process.wait()

        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Stopping DEX...{Colors.ENDC}")
            self.cleanup()
        except Exception as e:
            print(f"{Colors.FAIL}Error launching DEX: {e}{Colors.ENDC}")
            self.cleanup()

    def launch_dex_display2(self):
        """
        Launch DEX using display 2 (Miraclecast/Wireless Display method)
        This requires Miraclecast to be running
        """
        print(f"\n{Colors.HEADER}Launching Samsung DEX (Display 2 Mode){Colors.ENDC}")
        print(f"{Colors.WARNING}Make sure Miraclecast is running and connected{Colors.ENDC}")
        print(f"{Colors.WARNING}Press Ctrl+C to stop DEX{Colors.ENDC}\n")

        try:
            # Build scrcpy command for display 2
            cmd = [
                'scrcpy',
                '--display', '2',
                '--window-title=Samsung DEX',
                '--fullscreen',
                '--forward-all-clicks'
            ]

            # Launch scrcpy
            self.scrcpy_process = subprocess.Popen(cmd)

            # Wait for process
            self.scrcpy_process.wait()

        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Stopping DEX...{Colors.ENDC}")
            self.cleanup()
        except Exception as e:
            print(f"{Colors.FAIL}Error launching DEX: {e}{Colors.ENDC}")
            self.cleanup()

    def cleanup(self):
        """Clean up processes on exit"""
        if self.scrcpy_process:
            try:
                self.scrcpy_process.terminate()
                self.scrcpy_process.wait(timeout=5)
            except:
                self.scrcpy_process.kill()

        # Kill any remaining scrcpy processes
        subprocess.run(['pkill', 'scrcpy'],
                      stderr=subprocess.DEVNULL)

    def show_menu(self):
        """Display main menu"""
        while True:
            self.print_banner()

            print(f"{Colors.BOLD}Connection Methods:{Colors.ENDC}")
            print(f"  {Colors.OKBLUE}1.{Colors.ENDC} USB Connection (Recommended for setup)")
            print(f"  {Colors.OKBLUE}2.{Colors.ENDC} Wireless Connection (TCP/IP)")
            print(f"  {Colors.OKBLUE}3.{Colors.ENDC} Setup Wireless ADB (via USB first)")
            print(f"  {Colors.OKBLUE}4.{Colors.ENDC} Launch DEX with Miraclecast")
            print(f"  {Colors.OKBLUE}5.{Colors.ENDC} Exit")
            print()

            choice = input(f"{Colors.BOLD}Select option [1-5]: {Colors.ENDC}").strip()

            if choice == '1':
                if self.connect_adb_usb():
                    self.launch_dex_virtual_display()
            elif choice == '2':
                ip = input(f"\n{Colors.BOLD}Enter device IP address: {Colors.ENDC}").strip()
                port = input(f"{Colors.BOLD}Enter port [5555]: {Colors.ENDC}").strip()
                port = int(port) if port else 5555

                if self.connect_adb_tcpip(ip, port):
                    self.launch_dex_virtual_display()
            elif choice == '3':
                ip = self.enable_wireless_adb_via_usb()
                if ip:
                    input(f"\n{Colors.OKGREEN}Press Enter after unplugging USB cable...{Colors.ENDC}")
                    time.sleep(2)
                    if self.connect_adb_tcpip(ip):
                        input(f"\n{Colors.OKGREEN}Wireless ADB ready! Press Enter to continue...{Colors.ENDC}")
            elif choice == '4':
                print(f"\n{Colors.WARNING}This requires the TuxDex Miraclecast method{Colors.ENDC}")
                print(f"Run: {Colors.BOLD}python3 tuxdex.py{Colors.ENDC}")
                input(f"\nPress Enter to continue...")
            elif choice == '5':
                print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
                self.cleanup()
                sys.exit(0)
            else:
                print(f"{Colors.FAIL}Invalid option{Colors.ENDC}")
                time.sleep(1)

def main():
    """Main entry point"""
    launcher = DEXLauncher()

    # Set up signal handlers
    def signal_handler(sig, frame):
        print(f"\n{Colors.WARNING}Interrupted{Colors.ENDC}")
        launcher.cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Check dependencies
    launcher.print_banner()
    if not launcher.check_dependencies():
        sys.exit(1)

    time.sleep(2)

    # Show menu
    launcher.show_menu()

if __name__ == '__main__':
    main()
