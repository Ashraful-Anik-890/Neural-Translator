import sqlite3
from datetime import datetime

class HistoryDB:
    def __init__(self, db_name="translations.db"):
        # Connect to the database
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Creates the history table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT,
                translated_text TEXT,
                src_lang TEXT,
                target_lang TEXT,
                timestamp DATETIME
            )
        ''')
        self.conn.commit()

    def add_entry(self, source, translated, src_lang, target_lang):
        """Saves a translation."""
        self.cursor.execute('''
            INSERT INTO history (source_text, translated_text, src_lang, target_lang, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (source, translated, src_lang, target_lang, datetime.now()))
        self.conn.commit()

    def get_last_entries(self, limit=5):
        """Fetches the last N translations."""
        self.cursor.execute('''
            SELECT source_text, translated_text FROM history 
            ORDER BY id DESC LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()