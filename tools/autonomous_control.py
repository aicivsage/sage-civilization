#!/usr/bin/env python3
"""
Autonomous Desktop Control for Minetest Gameplay
Uses PowerShell for screenshots and Python automation
"""

import subprocess
import time
import os
from pathlib import Path

class DesktopController:
    """Control desktop via WSL2 -> Windows PowerShell bridge"""

    def __init__(self):
        self.screenshot_dir = "/mnt/c/temp/claude_screenshots"
        self.powershell_screenshot_script = "/tmp/take_screenshot.ps1"
        self._create_screenshot_script()
        self.target_window = "Minetest"  # Window title to focus

    def _create_screenshot_script(self):
        """Create PowerShell screenshot script"""
        script = """
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss_fff"
$outputPath = "C:\\temp\\claude_screenshots\\screenshot_$timestamp.png"
New-Item -ItemType Directory -Force -Path "C:\\temp\\claude_screenshots" | Out-Null
$bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

Write-Host "$outputPath"

$graphics.Dispose()
$bitmap.Dispose()
"""
        with open(self.powershell_screenshot_script, 'w') as f:
            f.write(script)

    def take_screenshot(self):
        """Take screenshot via PowerShell, return WSL path"""
        result = subprocess.run(
            ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', self.powershell_screenshot_script],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Extract path from output
        windows_path = result.stdout.strip()
        # Convert to WSL path
        wsl_path = windows_path.replace('C:\\', '/mnt/c/').replace('\\', '/')

        return wsl_path

    def mouse_move(self, x, y):
        """Move mouse to absolute coordinates"""
        ps_cmd = f"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point({x}, {y})"
        subprocess.run(['powershell.exe', '-Command', ps_cmd], check=True)

    def mouse_click(self, button='left', double=False):
        """Click mouse at current position"""
        # Use simpler SendInput approach via VBScript
        if button == 'left':
            button_code = '1'  # WScript.Shell SendKeys codes
        else:
            button_code = '2'

        # Create a simple VBS script to click
        vbs_script = f"""
Set WshShell = WScript.CreateObject("WScript.Shell")
Set objShell = CreateObject("Shell.Application")
WshShell.AppActivate "Minetest"
WScript.Sleep 100
"""
        # Write VBS to temp file
        vbs_path = "/tmp/click.vbs"
        with open(vbs_path, 'w') as f:
            f.write(vbs_script)

        # Use PowerShell's Add-Type to do actual mouse click
        ps_simple = '''
$signature = @"
[DllImport("user32.dll", CharSet=CharSet.Auto, CallingConvention=CallingConvention.StdCall)]
public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, uint dwExtraInfo);
"@
$SendMouseEvent = Add-Type -memberDefinition $signature -name "Win32MouseEventNew" -namespace Win32Functions -passThru
$SendMouseEvent::mouse_event(0x0002, 0, 0, 0, 0); Start-Sleep -Milliseconds 50; $SendMouseEvent::mouse_event(0x0004, 0, 0, 0, 0)
'''
        subprocess.run(['powershell.exe', '-Command', ps_simple], check=False)

    def focus_window(self, window_title=None):
        """Focus the target window before sending input"""
        if window_title is None:
            window_title = self.target_window

        ps_cmd = f"""
        Add-Type -AssemblyName Microsoft.VisualBasic
        Add-Type -AssemblyName System.Windows.Forms
        [Microsoft.VisualBasic.Interaction]::AppActivate('{window_title}')
        Start-Sleep -Milliseconds 200
        """
        subprocess.run(['powershell.exe', '-Command', ps_cmd], check=False)

    def keyboard_type(self, text, focus=True):
        """Type text via PowerShell SendKeys"""
        if focus:
            self.focus_window()

        # Escape special characters for PowerShell
        escaped = text.replace("'", "''").replace('"', '`"')
        ps_cmd = f"""
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait('{escaped}')
        """
        subprocess.run(['powershell.exe', '-Command', ps_cmd], check=True)

    def keyboard_press(self, key, modifiers=None, focus=True):
        """Press key or key combination"""
        if focus:
            self.focus_window()

        # SendKeys special keys mapping
        key_map = {
            'ENTER': '{ENTER}',
            'TAB': '{TAB}',
            'ESC': '{ESC}',
            'BACKSPACE': '{BACKSPACE}',
            'DELETE': '{DELETE}',
            'UP': '{UP}',
            'DOWN': '{DOWN}',
            'LEFT': '{LEFT}',
            'RIGHT': '{RIGHT}',
            'F10': '{F10}',
            'SPACE': ' ',
            'W': 'w',
            'A': 'a',
            'S': 's',
            'D': 'd'
        }

        send_key = key_map.get(key.upper(), key)

        if modifiers:
            # Ctrl = ^, Shift = +, Alt = %
            mod_map = {'ctrl': '^', 'shift': '+', 'alt': '%'}
            prefix = ''.join(mod_map.get(m.lower(), '') for m in modifiers.split('+'))
            send_key = f'{prefix}({send_key})'

        ps_cmd = f"""
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait('{send_key}')
        """
        subprocess.run(['powershell.exe', '-Command', ps_cmd], check=True)

    def get_screen_size(self):
        """Get screen dimensions"""
        ps_cmd = """
        Add-Type -AssemblyName System.Windows.Forms
        $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        Write-Host "$($screen.Width),$($screen.Height)"
        """
        result = subprocess.run(['powershell.exe', '-Command', ps_cmd], capture_output=True, text=True)
        w, h = result.stdout.strip().split(',')
        return int(w), int(h)


if __name__ == '__main__':
    # Test script
    print("Testing Desktop Controller...")

    controller = DesktopController()

    print("1. Getting screen size...")
    width, height = controller.get_screen_size()
    print(f"   Screen: {width}x{height}")

    print("2. Taking screenshot...")
    screenshot_path = controller.take_screenshot()
    print(f"   Screenshot saved: {screenshot_path}")
    print(f"   File exists: {os.path.exists(screenshot_path)}")

    print("\n✅ Desktop Controller ready for autonomous gameplay!")
    print(f"   Screenshot available at: {screenshot_path}")
