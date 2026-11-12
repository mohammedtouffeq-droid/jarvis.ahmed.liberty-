"""
J.A.R.V.I.S. Liberty // Global Dictation & Text Inscription Engine
Derived from isair/jarvis global dictation architecture.
Types live spoken text directly into the foreground application.
"""

import time
import pyautogui
from .config import load_settings

class DictationEngine:
    def __init__(self):
        self.settings = load_settings()

    def type_into_active_window(self, text: str, delay_before: float = 0.4) -> bool:
        """
        Types the text directly into whichever application window currently has focus.
        Safe, human-paced, and fully automated.
        """
        if not text:
            return False

        interval = self.settings.get("typing_delay", 0.02)
        try:
            # Short sleep to give the target window foreground focus
            time.sleep(delay_before)
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            print(f"[DictationEngine] Error typing: {e}")
            return False

    def press_key_combo(self, *keys) -> bool:
        """Triggers safe hotkeys (e.g. ctrl+s, win+d, enter)."""
        try:
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            print(f"[DictationEngine] Error triggering key combo: {e}")
            return False

# Global singleton
dictation_engine = DictationEngine()
