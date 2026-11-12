"""
J.A.R.V.I.S. Liberty // Modular Skill Registry
Derived from AnubhavChaturvedi jarvis-ai-assistant & leon-ai modular routing.
"""

import os
import subprocess
import webbrowser
import datetime
import pyautogui
from .speech import speech_engine
from .dictation import dictation_engine
from .guard import SystemGuard
from .memory import memory_store

APP_SHORTCUTS = {
    "chrome": "start chrome",
    "google": "start chrome",
    "youtube": "https://www.youtube.com",
    "yt": "https://www.youtube.com",
    "code": "code",
    "vscode": "code",
    "vs": "code",
    "notepad": "notepad",
    "calc": "calc",
    "calculator": "calc",
    "files": "explorer",
    "explorer": "explorer",
    "terminal": "start powershell",
    "cmd": "start cmd",
    "settings": "start ms-settings:",
    "spotify": "start spotify:",
    "skills": "https://www.skills.google",
    "arcade": "https://go.cloudskillsboost.google/arcade",
    "unstop": "https://unstop.com",
    "github": "https://github.com",
}

class SkillManager:
    @staticmethod
    def execute_skill(intent: str, payload: str = "") -> dict:
        intent = intent.lower().strip()

        # 1. Voice Dictation
        if intent in ["type", "write", "dictate"]:
            success = dictation_engine.type_into_active_window(payload)
            speech_engine.speak("Text inscribed into active window, Boss.")
            return {"status": "success", "message": f"Typed: '{payload}'"}

        # 2. App Launching
        if intent in ["open", "launch", "start"]:
            target = payload.lower().strip()
            if target in APP_SHORTCUTS:
                val = APP_SHORTCUTS[target]
                if val.startswith("http"):
                    webbrowser.open(val)
                else:
                    subprocess.Popen(val, shell=True)
                speech_engine.speak(f"Opening {target}, Boss.")
                return {"status": "success", "message": f"Launched {target}"}
            elif target.startswith("http"):
                webbrowser.open(target)
                speech_engine.speak("Opening requested destination, Boss.")
                return {"status": "success", "message": f"Navigated to {target}"}
            else:
                try:
                    subprocess.Popen(f"start {target}", shell=True)
                    speech_engine.speak(f"Starting {target}.")
                    return {"status": "success", "message": f"Started {target}"}
                except Exception as e:
                    return {"status": "error", "message": str(e)}

        # 3. Google Search
        if intent in ["search", "google"]:
            url = f"https://www.google.com/search?q={payload.replace(' ', '+')}"
            webbrowser.open(url)
            speech_engine.speak(f"Searching web for {payload}, Boss.")
            return {"status": "success", "message": f"Searched: {payload}"}

        # 4. YouTube
        if intent in ["youtube", "yt", "play"]:
            url = f"https://www.youtube.com/results?search_query={payload.replace(' ', '+')}"
            webbrowser.open(url)
            speech_engine.speak(f"Playing on YouTube, Boss.")
            return {"status": "success", "message": f"Streaming YouTube: {payload}"}

        # 5. Clean / Optimize RAM
        if intent in ["clean", "boost", "ram", "optimize"]:
            cleaned, before, after = SystemGuard.purge_memory()
            speech_engine.speak("Memory buffers purged. System stabilized, Boss.")
            return {"status": "success", "message": f"Purged {cleaned} files. RAM: {before}% -> {after}%"}

        # 6. Screenshot
        if intent in ["snap", "screenshot", "screen"]:
            dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
            out_path = os.path.join(desktop, f"JARVIS_Snapshot_{dt}.png")
            try:
                pyautogui.screenshot(out_path)
                speech_engine.speak("Snapshot secured to Desktop, Boss.")
                return {"status": "success", "message": f"Saved screenshot to {out_path}"}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        # 7. Stealth Focus
        if intent in ["stealth", "minimize"]:
            dictation_engine.press_key_combo('win', 'd')
            speech_engine.speak("Stealth mode active. All windows cleared, Boss.")
            return {"status": "success", "message": "Engaged Stealth Mode"}

        # 8. Motivation
        if intent in ["motivate", "motivation", "boost"]:
            msg = speech_engine.get_random_motivation()
            speech_engine.speak(msg)
            return {"status": "success", "message": msg}

        # 9. Time
        if intent in ["time", "date"]:
            now = datetime.datetime.now().strftime("%A, %I:%M %p")
            speech_engine.speak(f"It is {now}, Boss.")
            return {"status": "success", "message": f"Current Time: {now}"}

        # Fallback Search
        url = f"https://www.google.com/search?q={intent.replace(' ', '+')}"
        webbrowser.open(url)
        speech_engine.speak(f"Looking up {intent}, Boss.")
        return {"status": "success", "message": f"Routed query: {intent}"}
