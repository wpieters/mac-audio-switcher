#!/usr/bin/env python3
import subprocess
import rumps

class AudioSwitcherApp(rumps.App):
    def __init__(self):
        super().__init__("🔊")
        self.update_devices()

    def update_devices(self):
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
        
        # Set the menu
        self.menu.clear()
        for item in menu_items:
            self.menu.add(item)

    def get_audio_devices(self, device_type):
        try:
            cmd = ["switchaudiosource", "-a", "-t", device_type]
            output = subprocess.check_output(cmd).decode('utf-8')
            return [line.strip() for line in output.split('\n') if line.strip()]
        except:
            return []

    def get_current_device(self, device_type):
        try:
            cmd = ["switchaudiosource", "-c", "-t", device_type]
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
        try:
            subprocess.run(["switchaudiosource", "-s", device_name, "-t", device_type])
        except:
            pass

    @rumps.clicked("Refresh Devices")
    def refresh_clicked(self, _):
        self.update_devices()

if __name__ == "__main__":
    AudioSwitcherApp().run()
