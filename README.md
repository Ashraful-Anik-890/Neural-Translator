# Neural Translator

Modern, desktop translation agent with a clean CustomTkinter UI, realtime typing
translation and voice-to-voice capabilities.

---

## Table of Contents
- [About](#about)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## About

Neural Translator is a desktop application written in Python that provides fast, local
translation workflows with both text and voice support. It uses a modern CustomTkinter
interface (glass-like styling), supports theme switching, and keeps a local history of
translations.

## Features

- Modern CustomTkinter UI with dark/light themes
- Real-time translation as you type (debounced input)
- Voice input and text-to-speech output (SpeechRecognition + pyttsx3)
- Local history stored in SQLite via `history_db.py`
- Copy-to-clipboard and responsive, multithreaded UI for smooth performance

## Project Structure

- `main.py` — Application GUI (frontend)
- `translator_engine.py` — Translation logic and API wrappers
- `audio_manager.py` — Microphone and speaker helpers
- `history_db.py` — SQLite history manager
- `requirment.text` — Dependency list (install with pip)
- `README.md` — This file

> Note: The repository currently contains `requirment.text` (typo). Use that file
> when installing dependencies or rename it to `requirements.txt` if you prefer.

## Installation

Prerequisites:

- Python 3.8+
- (Optional) Virtual environment recommended

Clone the repository:

```powershell
git clone <repo-url>
cd Neural-Translator
```

Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell run:

```powershell
pip install -r requirements.txt
```

Linux note: for microphone support you may need system packages (example for Debian/Ubuntu):

```bash
sudo apt-get install python3-pyaudio portaudio19-dev
```

## Usage

Run the app:

```powershell
python main.py
```

Usage tips:

- Type in the text box to translate automatically (debounced input).
- Click the microphone button to speak and translate.
- Click the speaker button to hear the translated text.
- Use the theme switch to toggle dark/light modes.

## Troubleshooting

- ImportError: cannot import name 'HistoryDB'
	- Ensure the file is named `history_db.py` and that your PYTHONPATH includes the
		project directory.

- PyAudio installation failures
	- Windows: try installing the appropriate `.whl` for your Python version or
		install Visual C++ Build Tools.
	- macOS: `brew install portaudio` then `pip install pyaudio`.
	- Linux: install PortAudio and development headers, e.g. `portaudio19-dev`.

## Tech Stack

- GUI: CustomTkinter
- Translation: deep-translator (or other API adapters in `translator_engine.py`)
- Audio: SpeechRecognition, pyttsx3, PyAudio
- DB: sqlite3 (standard library)

## Contributing

Contributions are welcome. Open an issue or submit a pull request with a clear
description of changes and testing steps.

## License

This project is available under the MIT License.

## Author

Built by MD. Ashraful Al Amin
