🧠 Neural Translator

Neural Translator is a modern, desktop-based translation agent built with Python. It moves beyond simple script-based tools by offering a responsive "Glassmorphism" UI, real-time typing translation, and full voice-to-voice conversational capabilities.

Designed with CustomTkinter, it features a sleek dark/light mode interface that looks native on Windows, macOS, and Linux.

✨ Key Features

🎨 Modern UI: Built with CustomTkinter for a high-DPI, rounded-corner aesthetic.

🌗 Adaptive Theme: Toggle between Dark Mode and Light Mode instantly.

⚡ Real-Time Translation: "Debounce" logic translates as you type (no submit button needed).

🗣️ Voice-to-Voice: * Mic Input: Speak to translate (SpeechRecognition).

TTS Output: Listen to translations (pyttsx3).

💾 Local History: Automatically saves your translation history to a local SQLite database.

📋 Quick Tools: One-click copy to clipboard.

🚀 Multi-Threaded: The UI remains buttery smooth (60fps) even while fetching data from the API.

📂 Project Structure

NeuralTranslator/
│
├── main.py              # 🖥️ The Application GUI (Frontend)
├── translator_engine.py # 🧠 Translation Logic (API Wrapper)
├── audio_manager.py     # 🎤 Microphone & Speaker Handler
├── history_db.py        # 💾 SQLite Database Manager
├── requirements.txt     # 📦 Dependency List
└── README.md          


🛠️ Installation

1. Prerequisites

Python 3.8 or higher is installed.

(Optional but recommended) A virtual environment.

2. Clone the Repository


3. Install Dependencies

Run the following command to install all required libraries:

pip install -r requirements.txt


Note for Linux Users: You may need to install portaudio separately for the microphone to work:
sudo apt-get install python3-pyaudio portaudio19-dev

🚀 Usage

To start the application, simply run the main.py file:

python main.py


Type in the left box to translate automatically.

Click 🎤 Speak to use your microphone.

Click 🔊 Listen to hear the pronunciation.

Use the Switch in the top right to change themes.

🧩 Tech Stack

GUI: CustomTkinter

Translation: deep-translator

Audio: SpeechRecognition, pyttsx3, pyaudio

Database: sqlite3 (Standard Library)

System: threading, pyperclip

🐛 Troubleshooting common errors

ImportError: cannot import name 'HistoryDB'

Make sure your database file is named exactly history_db.py and not historyy_db.py or HistortDB.py.

PyAudio fails to install

Windows: If pip install pyaudio fails, try downloading the specific .whl file for your Python version from here, or install Visual C++ Build Tools.

Mac/Linux: Ensure you have portaudio installed via Homebrew (brew install portaudio) or APT.

📜 License

This project is open-source and available under the MIT License.

👨‍💻 Author

Built with Python & Coffee by MD. Ashraful Al Amin