# Audio Switcher

A simple macOS menu bar application that allows quick switching between audio input and output devices.

## Requirements

- Python 3.6+
- `rumps` library for the menu bar interface
- `switchaudio-osx` for controlling audio devices

## Installation

1. Install the required Python package:
```bash
pip install -r requirements.txt
```

2. Install switchaudio-osx using Homebrew:
```bash
brew install switchaudio-osx
```

3. Make the script executable:
```bash
chmod +x audio_switcher.py
```

## Usage

Simply run:
```bash
./audio_switcher.py
```

The app will appear in your menu bar with a speaker icon (🔊). Click it to:
- View and switch between available output devices
- View and switch between available input devices
- Refresh the device list

## Features

- Shows all available audio input and output devices
- Indicates currently selected devices with a checkmark
- Allows quick switching between devices
- Provides a refresh option to update the device list
