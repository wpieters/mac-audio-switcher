from setuptools import setup

APP = ['audio_switcher.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,
    'plist': {
        'LSUIElement': True,
        'CFBundleName': 'Audio Switcher',
        'CFBundleDisplayName': 'Audio Switcher',
        'CFBundleIdentifier': 'dev.wpieters.audio-switcher',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
    },
    'packages': ['rumps'],
    'includes': ['subprocess'],
    'excludes': ['tkinter', 'matplotlib', 'PIL'],
    'site_packages': True,
    'strip': True,
    'semi_standalone': True,  # This should help with framework issues
}

setup(
    app=APP,
    name="Audio Switcher",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['rumps'],
)
