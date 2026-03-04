# PCWatcher

A Windows system monitor that tracks CPU, memory, and disk usage, with desktop notifications via PushMe.

## Features

- Real-time monitoring of CPU, memory, and disk usage
- Desktop notifications via PushMe when thresholds are exceeded
- System tray integration for background running
- Configurable thresholds via GUI
- Automatic startup option

## Requirements

- Python 3.8+
- Windows OS

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python pcwatcher.py
```

## Configuration

Edit `config.json` or use the built-in GUI to set monitoring thresholds:
- CPU usage threshold (%)
- Memory usage threshold (%)
- Disk usage threshold (%)
- Check interval (seconds)
- PushMe API key

## Building

```bash
pyinstaller build.spec
```

## License

MIT License
