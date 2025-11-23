from deep_translator import GoogleTranslator
import threading

class TranslatorEngine:
    def __init__(self):
        self.source_lang = 'auto'
        self.target_lang = 'es' # Default to Spanish

    def translate_text(self, text, target, source='auto'):
        """
        Translates text with error handling.
        """
        try:
            translator = GoogleTranslator(source=source, target=target)
            result = translator.translate(text)
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def get_supported_languages(self):
        """Returns a dict of supported languages for the UI dropdown."""
        return GoogleTranslator().get_supported_languages(as_dict=True)