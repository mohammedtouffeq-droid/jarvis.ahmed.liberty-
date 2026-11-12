"""
J.A.R.V.I.S. Liberty // Controller & Intent Dispatcher
Derived from OpenInterpreter & self-operating-computer dispatch models.
Parses natural language directives into secure actions.
"""

from .guard import SystemGuard
from .skills import SkillManager
from .memory import memory_store
from .speech import speech_engine

class ActionDispatcher:
    def __init__(self):
        self.guard = SystemGuard()

    def dispatch(self, raw_input: str) -> dict:
        text = raw_input.strip()
        if not text:
            return {"status": "empty", "message": "No command provided."}

        # 1. Security Check
        is_safe, reason = self.guard.validate_action(text)
        if not is_safe:
            speech_engine.speak("Security alert: That operation is restricted for your safety, Boss.")
            return {"status": "blocked", "message": f"❌ {reason}"}

        # 2. Parse Intent and Payload
        text_lower = text.lower()

        # Voice Dictation (type / write)
        if text_lower.startswith("type ") or text_lower.startswith("write "):
            payload = text[text.find(" ") + 1:].strip()
            res = SkillManager.execute_skill("type", payload)
            memory_store.add_interaction(text, res.get("message", ""), "type")
            return res

        # App Launch
        if text_lower.startswith("open ") or text_lower.startswith("launch "):
            payload = text_lower[text_lower.find(" ") + 1:].strip()
            res = SkillManager.execute_skill("open", payload)
            memory_store.add_interaction(text, res.get("message", ""), "launch")
            return res

        # Web Search
        if text_lower.startswith("search ") or text_lower.startswith("google "):
            payload = text[text.find(" ") + 1:].strip()
            res = SkillManager.execute_skill("search", payload)
            memory_store.add_interaction(text, res.get("message", ""), "search")
            return res

        # YouTube
        if text_lower.startswith("yt ") or text_lower.startswith("youtube ") or text_lower.startswith("play "):
            payload = text[text.find(" ") + 1:].strip()
            res = SkillManager.execute_skill("youtube", payload)
            memory_store.add_interaction(text, res.get("message", ""), "media")
            return res

        # Single word triggers
        if text_lower in ["clean", "boost", "ram", "optimize"]:
            res = SkillManager.execute_skill("clean")
            memory_store.add_interaction(text, res.get("message", ""), "clean")
            return res

        if text_lower in ["snap", "screenshot", "screen"]:
            res = SkillManager.execute_skill("snap")
            memory_store.add_interaction(text, res.get("message", ""), "snapshot")
            return res

        if text_lower in ["stealth", "minimize"]:
            res = SkillManager.execute_skill("stealth")
            memory_store.add_interaction(text, res.get("message", ""), "stealth")
            return res

        if text_lower in ["motivate", "motivation", "boost"]:
            res = SkillManager.execute_skill("motivate")
            memory_store.add_interaction(text, res.get("message", ""), "motivate")
            return res

        if text_lower in ["time", "date"]:
            res = SkillManager.execute_skill("time")
            memory_store.add_interaction(text, res.get("message", ""), "time")
            return res

        # Fallback query
        res = SkillManager.execute_skill(text)
        memory_store.add_interaction(text, res.get("message", ""), "fallback")
        return res

# Global singleton
dispatcher = ActionDispatcher()
