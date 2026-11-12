"""
J.A.R.V.I.S. Liberty // Local Knowledge Graph & Memory Store
Derived from isair/jarvis local persistent memory design.
Saves session notes, user goals, and interaction logs locally.
"""

import json
import time
from pathlib import Path
from .config import DATA_DIR

MEMORY_FILE = DATA_DIR / "memory.json"

DEFAULT_MEMORY = {
    "goals": [
        "Gift a brand-new self-start car/bike for Father to replace 15-year old vehicle",
        "Retire Father from 8-year continuous night shifts",
        "Master high-income software engineering and automation systems"
    ],
    "history": [],
    "notes": []
}

class MemoryStore:
    def __init__(self):
        self.data = self._load()

    def _load(self) -> dict:
        if not MEMORY_FILE.exists():
            self._save(DEFAULT_MEMORY)
            return DEFAULT_MEMORY.copy()
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_MEMORY.copy()

    def _save(self, data: dict):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add_interaction(self, user_text: str, jarvis_reply: str, action: str = ""):
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_text,
            "jarvis": jarvis_reply,
            "action": action
        }
        self.data["history"].append(entry)
        # Keep last 150 interactions
        self.data["history"] = self.data["history"][-150:]
        self._save(self.data)

    def add_note(self, note: str):
        self.data["notes"].append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": note
        })
        self._save(self.data)

    def get_goals(self) -> list:
        return self.data.get("goals", [])

    def get_recent_history(self, limit: int = 10) -> list:
        return self.data.get("history", [])[-limit:]

# Global singleton
memory_store = MemoryStore()
