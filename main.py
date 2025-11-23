import customtkinter as ctk
from translator_engine import TranslatorEngine
from audio_manager import AudioManager
from history_db import HistoryDB
import pyperclip
import threading

# --- Config & Setup ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class ModernTranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Initialize the Brains (Backend)
        self.engine = TranslatorEngine()
        self.audio = AudioManager()
        self.db = HistoryDB()

        # 2. Window Configuration
        self.title("Neural Translator")  # Renamed as requested
        self.geometry("950x650")
        
        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- HEADER SECTION ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.lbl_title = ctk.CTkLabel(self.header_frame, text="Neural Translator", font=("Roboto Medium", 22))
        self.lbl_title.pack(side="left", padx=20)

        # Feature: Light/Dark Mode Toggle
        self.switch_var = ctk.StringVar(value="on")
        self.mode_switch = ctk.CTkSwitch(self.header_frame, text="Dark Mode", command=self.toggle_mode, 
                                         variable=self.switch_var, onvalue="on", offvalue="off")
        self.mode_switch.pack(side="right", padx=20)

        # --- CONTROLS SECTION ---
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.grid(row=0, column=0, columnspan=2, pady=(60,0))

        self.langs = self.engine.get_supported_languages()
        self.lang_names = list(self.langs.keys())

        self.source_combo = ctk.CTkComboBox(self.control_frame, values=["auto"] + self.lang_names, width=150)
        self.source_combo.set("auto")
        self.source_combo.pack(side="left", padx=10)

        self.lbl_arrow = ctk.CTkLabel(self.control_frame, text="➜", font=("Arial", 20))
        self.lbl_arrow.pack(side="left", padx=5)

        self.target_combo = ctk.CTkComboBox(self.control_frame, values=self.lang_names, width=150)
        self.target_combo.set("spanish")
        self.target_combo.pack(side="left", padx=10)

        # --- INPUT/OUTPUT SECTION ---
        
        # Left Side: Input
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")
        
        self.input_text = ctk.CTkTextbox(self.input_frame, font=("Arial", 16), corner_radius=10)
        self.input_text.pack(expand=True, fill="both")
        
        # Feature: Ghost Text (Placeholder Logic)
        self.placeholder = "Type here to translate..."
        self.input_text.insert("0.0", self.placeholder)
        self.input_text.configure(text_color="gray")
        self.input_text.bind("<FocusIn>", self.on_entry_click)
        self.input_text.bind("<FocusOut>", self.on_focus_out)
        self.input_text.bind("<KeyRelease>", self.start_debounce_translation)

        # Right Side: Output
        self.output_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.output_frame.grid(row=1, column=1, padx=15, pady=10, sticky="nsew")

        self.output_text = ctk.CTkTextbox(self.output_frame, font=("Arial", 16), corner_radius=10, fg_color=("gray85", "#2b2b2b"))
        self.output_text.pack(expand=True, fill="both")
        self.output_text.configure(state="disabled")

        # --- FOOTER / ACTIONS ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=2, column=0, columnspan=2, pady=20)

        # Buttons with connected Logic
        self.btn_mic = ctk.CTkButton(self.action_frame, text="🎤 Speak", command=self.start_listening, width=100, fg_color="#c0392b")
        self.btn_mic.pack(side="left", padx=10)

        self.btn_translate = ctk.CTkButton(self.action_frame, text="Translate", command=self.perform_translation, width=120)
        self.btn_translate.pack(side="left", padx=10)

        self.btn_speak = ctk.CTkButton(self.action_frame, text="🔊 Listen", command=self.speak_output, width=100, fg_color="#2980b9")
        self.btn_speak.pack(side="left", padx=10)

        self.btn_copy = ctk.CTkButton(self.action_frame, text="📋 Copy", command=self.copy_to_clipboard, width=80, fg_color="gray")
        self.btn_copy.pack(side="left", padx=10)

        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.timer = None

    # --- EVENT HANDLERS ---

    def toggle_mode(self):
        if self.switch_var.get() == "on":
            ctk.set_appearance_mode("Dark")
            self.mode_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("Light")
            self.mode_switch.configure(text="Light Mode")

    def on_entry_click(self, event):
        """Clears placeholder when user clicks inside."""
        current_text = self.input_text.get("0.0", "end-1c")
        if current_text == self.placeholder:
            self.input_text.delete("0.0", "end")
            self.input_text.configure(text_color=("black", "white")) # Adjust for Light/Dark mode

    def on_focus_out(self, event):
        """Restores placeholder if empty."""
        if self.input_text.get("0.0", "end-1c").strip() == "":
            self.input_text.insert("0.0", self.placeholder)
            self.input_text.configure(text_color="gray")

    def start_listening(self):
        """Connects to audio_manager.py"""
        self.status_label.configure(text="Listening... speak now!", text_color="#e74c3c")
        
        def _listen_thread():
            text = self.audio.listen() # Uses the module you have!
            if text:
                # Need to use 'after' to update UI from thread safely
                self.after(0, lambda: self._update_input_after_listen(text))
            else:
                self.after(0, lambda: self.status_label.configure(text="Could not hear you.", text_color="gray"))
        
        threading.Thread(target=_listen_thread).start()

    def _update_input_after_listen(self, text):
        self.input_text.delete("0.0", "end")
        self.input_text.insert("0.0", text)
        self.input_text.configure(text_color=("black", "white"))
        self.perform_translation()

    def speak_output(self):
        """Connects to audio_manager.py"""
        text = self.output_text.get("1.0", "end-1c")
        if text.strip():
            self.audio.speak(text) # Uses the module you have!

    def start_debounce_translation(self, event):
        if self.timer:
            self.after_cancel(self.timer)
        self.timer = self.after(1000, self.perform_translation)

    def perform_translation(self):
        text = self.input_text.get("1.0", "end-1c")
        # Don't translate the placeholder
        if text == self.placeholder or not text.strip():
            return

        target = self.target_combo.get()
        source = self.source_combo.get()
        target_code = self.langs.get(target, 'es')
        source_code = self.langs.get(source, 'auto')

        self.status_label.configure(text="Translating...", text_color="#f39c12")
        
        # Pass necessary data to thread
        threading.Thread(target=self._run_translation_thread, 
                         args=(text, target_code, source_code, target)).start()

    def _run_translation_thread(self, text, target_code, source_code, target_lang_name):
        result = self.engine.translate_text(text, target_code, source_code)
        
        # Update UI safely
        self.after(0, lambda: self._update_output(result))
        
        # Connects to history_db.py
        self.db.add_entry(text, result, source_code, target_lang_name) 

    def _update_output(self, result):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.output_text.configure(state="disabled")
        self.status_label.configure(text="Translation Saved.", text_color="green")

    def copy_to_clipboard(self):
        text = self.output_text.get("1.0", "end-1c")
        pyperclip.copy(text)
        self.status_label.configure(text="Copied to Clipboard", text_color="gray")

if __name__ == "__main__":
    app = ModernTranslatorApp()
    app.mainloop()