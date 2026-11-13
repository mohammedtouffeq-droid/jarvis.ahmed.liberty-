"""
J.A.R.V.I.S. Liberty // Controller & Intent Dispatcher
Synthesized from OpenInterpreter, leon-ai, and self-operating-computer dispatch models.
Parses natural language directives into secure actions for Boss Ahmed.
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

        # 1. Security Guardrail Check
        is_safe, reason = self.guard.validate_action(text)
        if not is_safe:
            speech_engine.speak("Security alert: That operation is restricted for your safety, Boss.")
            return {"status": "blocked", "message": f"❌ {reason}"}

        text_lower = text.lower()

        # 2. Voice Dictation (type / write)
        if text_lower.startswith("type ") or text_lower.startswith("write "):
            payload = text[text.find(" ") + 1:].strip()
            res = SkillManager.execute_skill("type", payload)
            memory_store.add_interaction(text, res.get("message", ""), "type")
            return res

        # 3. Math & Calculation (calc / what is 50*20)
        if text_lower.startswith("calc ") or text_lower.startswith("calculate "):
            payload = text[text.find(" ") + 1:].strip()
            res = SkillManager.execute_skill("calc", payload)
            memory_store.add_interaction(text, res.get("message", ""), "math")
            return res

        # 4. Wikipedia & Knowledge (wiki / who is / what is)
        if text_lower.startswith("wiki ") or text_lower.startswith("who is ") or text_lower.startswith("what is "):
            for prefix in ["wiki ", "who is ", "what is "]:
                if text_lower.startswith(prefix):
                    payload = text[len(prefix):].strip()
                    break
            res = SkillManager.execute_skill("wiki", payload)
            memory_store.add_interaction(text, res.get("message", ""), "knowledge")
            return res

        # 5. Weather
        if text_lower.startswith("weather ") or text_lower == "weather":
            payload = text[text.find(" ") + 1:].strip() if " " in text else ""
            res = SkillManager.execute_skill("weather", payload)
            memory_store.add_interaction(text, res.get("message", ""), "weather")
            return res

        # 6. App Launch
        if text_lower.startswith("open ") or text_lower.startswith("launch ") or text_lower.startswith("start "):
            payload = text_lower[text_lower.find(" ") + 1:].strip()
            res = SkillManager.execute_skill("open", payload)
            memory_store.add_interaction(text, res.get("message", ""), "launch")
            return res

        # 7. Web Search
        if text_lower.startswith("search ") or text_lower.startswith("google "):
            payload = text[text.find(" ") + 1:].strip()
            res = SkillManager.execute_skill("search", payload)
            memory_store.add_interaction(text, res.get("message", ""), "search")
            return res

        # 8. YouTube
        if text_lower.startswith("yt ") or text_lower.startswith("youtube ") or text_lower.startswith("play "):
            payload = text[text.find(" ") + 1:].strip()
            res = SkillManager.execute_skill("youtube", payload)
            memory_store.add_interaction(text, res.get("message", ""), "media")
            return res

        # 9. Hardware & System Volume
        if text_lower in ["volume up", "volup", "sound up"]:
            res = SkillManager.execute_skill("volup")
            memory_store.add_interaction(text, res.get("message", ""), "volume")
            return res

        if text_lower in ["volume down", "voldown", "sound down"]:
            res = SkillManager.execute_skill("voldown")
            memory_store.add_interaction(text, res.get("message", ""), "volume")
            return res

        if text_lower in ["mute", "unmute", "silence"]:
            res = SkillManager.execute_skill("mute")
            memory_store.add_interaction(text, res.get("message", ""), "volume")
            return res

        # 10. Screen Scrolling
        if text_lower in ["scroll up", "scrollup", "page up"]:
            res = SkillManager.execute_skill("scroll up")
            return res

        if text_lower in ["scroll down", "scrolldown", "page down"]:
            res = SkillManager.execute_skill("scroll down")
            return res

        # 11. Security Lock Workstation
        if text_lower in ["lock", "lock screen", "lock pc", "lock computer"]:
            res = SkillManager.execute_skill("lock")
            memory_store.add_interaction(text, res.get("message", ""), "security")
            return res

        # 12. Single Word Quick Triggers
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

        if text_lower in ["empty bin", "clean trash", "empty trash"]:
            res = SkillManager.execute_skill("empty bin")
            memory_store.add_interaction(text, res.get("message", ""), "maintenance")
            return res

        if text_lower in ["specs", "system", "ip", "specs check"]:
            res = SkillManager.execute_skill("specs")
            memory_store.add_interaction(text, res.get("message", ""), "system")
            return res

        if text_lower in ["joke", "funny", "tell me a joke"]:
            res = SkillManager.execute_skill("joke")
            memory_store.add_interaction(text, res.get("message", ""), "humor")
            return res

        if text_lower in ["motivate", "motivation", "boost"]:
            res = SkillManager.execute_skill("motivate")
            memory_store.add_interaction(text, res.get("message", ""), "motivate")
            return res

        if text_lower in ["time", "date"]:
            res = SkillManager.execute_skill("time")
            memory_store.add_interaction(text, res.get("message", ""), "time")
            return res

        # Fallback Query
        res = SkillManager.execute_skill(text)
        memory_store.add_interaction(text, res.get("message", ""), "fallback")
        return res

# Global singleton
dispatcher = ActionDispatcher()
