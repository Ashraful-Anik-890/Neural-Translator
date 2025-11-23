import speech_recognition as sr
import pyttsx3
import threading

class AudioManager:
    def __init__(self):
        # Initialize Text-to-Speech engine
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150) 
        except Exception as e:
            print(f"Warning: TTS Engine could not start: {e}")
            self.engine = None

        # Initialize Recognizer
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        """Speaks the text in a separate thread."""
        if not self.engine:
            return

        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
        
        threading.Thread(target=_speak).start()

    def listen(self):
        """Listens to the microphone and returns text."""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                # Listen with a timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.WaitTimeoutError:
                return None 
            except sr.UnknownValueError:
                return None 
            except Exception as e:
                print(f"Mic Error: {e}")
                return None