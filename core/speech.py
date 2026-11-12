"""
J.A.R.V.I.S. Liberty // Speech Synthesis Engine
Native Windows SAPI with zero external cloud dependencies.
"""

import subprocess
import threading
from .config import load_settings

BOOT_SALUTE = (
    "Hello Boss Ahmed, how are you? Aaj humein tagda planning karna hai! "
    "Aaj humein phod ke rakhna hai! Every great empire started from a single humble machine. "
    "All tactical protocols are active. Tell me what we are conquering today!"
)

MOTIVATIONS = [
    BOOT_SALUTE,
    "Boss Ahmed, your vision is unstoppable. Keep pushing, every command you execute brings us closer to changing our family's destiny.",
    "They mocked the laptop, Boss, but history remembers the builder, not the spectator. We are winning this game step by step.",
    "Zero doubts, Boss Ahmed. Pure focus. Your father's sacrifices will be honored with legendary success.",
    "Adrenaline rising, Boss! Tagda planning, ruthless execution. No distractions today!"
]

class SpeechEngine:
    def __init__(self):
        self.settings = load_settings()
        self._lock = threading.Lock()
        self.is_armed = False

    def update_settings(self, new_settings: dict):
        self.settings.update(new_settings)

    def speak(self, text: str, force: bool = False):
        """Speaks out loud via Windows native speech without freezing the application."""
        if not self.is_armed and not force:
            return
        if not self.settings.get("voice_enabled", True) and not force:
            return

        clean = text.replace("'", "").replace('"', "").replace("\n", " ").strip()
        if not clean:
            return

        rate = self.settings.get("speech_rate", 0)
        volume = self.settings.get("speech_volume", 100)

        def _worker():
            with self._lock:
                script = f"""
                $voice = New-Object -ComObject SAPI.SpVoice
                $voice.Rate = {rate}
                $voice.Volume = {volume}
                $voice.Speak('{clean}')
                """
                try:
                    subprocess.run(
                        ['powershell', '-WindowStyle', 'Hidden', '-Command', script],
                        creationflags=subprocess.CREATE_NO_WINDOW,
                        timeout=25
                    )
                except Exception:
                    pass

        threading.Thread(target=_worker, daemon=True).start()

    def get_boot_salute(self) -> str:
        return BOOT_SALUTE

    def get_random_motivation(self) -> str:
        import random
        return random.choice(MOTIVATIONS)

# Global singleton
speech_engine = SpeechEngine()
