"""
J.A.R.V.I.S. Liberty // Configuration Matrix
Operator: Boss Ahmed
Lightweight, Zero-Cost, Modular Architecture
"""

import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "operator_name": "Boss Ahmed",
    "voice_enabled": True,
    "speech_rate": 0,           # SAPI Rate: -10 to +10
    "speech_volume": 100,       # 0 to 100
    "wake_word": "jarvis",
    "auto_dictation": True,
    "typing_delay": 0.02,
    "safety_mode": True,
    "port": 7777,
    "host": "127.0.0.1"
}

def load_settings() -> dict:
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            merged = DEFAULT_SETTINGS.copy()
            merged.update(data)
            return merged
    except Exception:
        return DEFAULT_SETTINGS.copy()

def save_settings(settings: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)
