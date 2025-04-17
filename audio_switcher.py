#!/usr/bin/env python3
import subprocess
import os
import rumps

class AudioSwitcherApp(rumps.App):
    def __init__(self):
        super().__init__("🔊")
        # Find switchaudio-osx command
        self.switcher_cmd = self.find_switcher_cmd()
        if not self.switcher_cmd:
            rumps.alert(title="Error", message="Could not find switchaudio-osx command. Please make sure it's installed via Homebrew or Nix.")
        self.update_devices()

    def find_switcher_cmd(self):
        # Common paths for Homebrew and Nix
        paths = [
            "/opt/homebrew/bin/switchaudiosource",  # Homebrew on Apple Silicon
            "/usr/local/bin/switchaudiosource",     # Homebrew on Intel
            "/run/current-system/sw/bin/switchaudiosource",  # NixOS
            os.path.expanduser("~/.nix-profile/bin/switchaudiosource"),  # Nix user profile
        ]
        for path in paths:
            if os.path.exists(path):
                return path
        return None

    def update_devices(self):
        if not self.switcher_cmd:
            return
            
        # Get input devices
        input_devices = self.get_audio_devices("input")
        current_input = self.get_current_device("input")
        
        # Get output devices
        output_devices = self.get_audio_devices("output")
        current_output = self.get_current_device("output")

        # Build menu items list
        menu_items = []
        
        # Add output devices section
        menu_items.append(rumps.MenuItem("Output Devices:"))
        for device in output_devices:
            item = rumps.MenuItem(device, callback=self.switch_output_device)
            item.state = 1 if device == current_output else 0
            menu_items.append(item)

        # Add separator
        menu_items.append(None)

        # Add input devices section
        menu_items.append(rumps.MenuItem("Input Devices:"))
        for device in input_devices:
            item = rumps.MenuItem(device, callback=self.switch_input_device)
            item.state = 1 if device == current_input else 0
            menu_items.append(item)

        # Add separator and refresh button
        menu_items.append(None)
        menu_items.append(rumps.MenuItem("Refresh Devices", callback=self.refresh_clicked))
        
        # Add separator and quit button
        menu_items.append(None)
        menu_items.append(rumps.MenuItem("Quit", callback=self.quit_clicked))
        
        # Set the menu
        self.menu.clear()
        for item in menu_items:
            self.menu.add(item)

    def get_audio_devices(self, device_type):
        if not self.switcher_cmd:
            return []
        try:
            cmd = [self.switcher_cmd, "-a", "-t", device_type]
            output = subprocess.check_output(cmd).decode('utf-8')
            return [line.strip() for line in output.split('\n') if line.strip()]
        except:
            return []

    def get_current_device(self, device_type):
        if not self.switcher_cmd:
            return None
        try:
            cmd = [self.switcher_cmd, "-c", "-t", device_type]
            return subprocess.check_output(cmd).decode('utf-8').strip()
        except:
            return None

    def switch_output_device(self, sender):
        self.switch_device(sender.title, "output")
        self.update_devices()

    def switch_input_device(self, sender):
        self.switch_device(sender.title, "input")
        self.update_devices()

    def switch_device(self, device_name, device_type):
        if not self.switcher_cmd:
            return
        try:
            subprocess.run([self.switcher_cmd, "-s", device_name, "-t", device_type])
        except:
            pass

    @rumps.clicked("Refresh Devices")
    def refresh_clicked(self, _):
        self.update_devices()

    @rumps.clicked("Quit")
    def quit_clicked(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    AudioSwitcherApp().run()
