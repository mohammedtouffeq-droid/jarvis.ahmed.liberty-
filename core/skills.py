"""
J.A.R.V.I.S. Liberty // Modular Skill Registry
Synthesized from AnubhavChaturvedi jarvis-ai-assistant, leon-ai, OpenInterpreter,
Robee99/PersonalJarvis, and OthersideAI self-operating-computer.
"""

import os
import ast
import json
import socket
import datetime
import subprocess
import webbrowser
import urllib.request
import urllib.parse
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

TECH_JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs, Boss!",
    "There are 10 types of people in the world: those who understand binary, and those who do not.",
    "A SQL query walks into a bar, walks up to two tables and asks: Can I join you?",
    "Why was the JavaScript developer sad? Because he did not Node how to Express himself!",
    "Hardware is the part of a computer that you can kick; software is the part you can only curse at, Boss!"
]

def safe_math_eval(expr: str):
    """Safely evaluates basic arithmetic expressions without eval() vulnerability."""
    allowed_operators = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.Mod: lambda a, b: a % b,
        ast.Pow: lambda a, b: a ** b,
        ast.USub: lambda a: -a,
        ast.UAdd: lambda a: +a,
    }

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](left, right)
            raise ValueError(f"Unsupported operator: {op_type}")
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](operand)
            raise ValueError(f"Unsupported operator: {op_type}")
        raise ValueError("Invalid mathematical expression")

    cleaned = expr.replace("x", "*").replace("^", "**")
    tree = ast.parse(cleaned, mode='eval')
    return _eval(tree)


class SkillManager:
    @staticmethod
    def execute_skill(intent: str, payload: str = "") -> dict:
        intent = intent.lower().strip()

        # 1. Voice Dictation & Direct Typing (isair/jarvis + self-operating-computer)
        if intent in ["type", "write", "dictate"]:
            success = dictation_engine.type_into_active_window(payload)
            speech_engine.speak("Text inscribed into active window, Boss.")
            return {"status": "success", "message": f"Typed: '{payload}'"}

        # 2. Application & Web Launcher (PersonalJarvis + AnubhavChaturvedi)
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

        # 3. Google Intelligence Search
        if intent in ["search", "google"]:
            url = f"https://www.google.com/search?q={urllib.parse.quote_plus(payload)}"
            webbrowser.open(url)
            speech_engine.speak(f"Searching web for {payload}, Boss.")
            return {"status": "success", "message": f"Searched: {payload}"}

        # 4. YouTube Autoplay
        if intent in ["youtube", "yt", "play"]:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(payload)}"
            webbrowser.open(url)
            speech_engine.speak("Streaming on YouTube, Boss.")
            return {"status": "success", "message": f"Streaming YouTube: {payload}"}

        # 5. Volume Controls (Sanjay-AI-Assistant / psycoks)
        if intent in ["volup", "volume up", "increase volume"]:
            pyautogui.press('volumeup', presses=5)
            speech_engine.speak("Volume increased, Boss.")
            return {"status": "success", "message": "Master volume raised (+10%)"}

        if intent in ["voldown", "volume down", "decrease volume"]:
            pyautogui.press('volumedown', presses=5)
            speech_engine.speak("Volume lowered, Boss.")
            return {"status": "success", "message": "Master volume lowered (-10%)"}

        if intent in ["mute", "unmute", "silence"]:
            pyautogui.press('volumemute')
            return {"status": "success", "message": "Audio toggle (Mute/Unmute)"}

        # 6. Screen Scrolling (self-operating-computer)
        if intent in ["scroll up", "scrollup"]:
            pyautogui.scroll(500)
            return {"status": "success", "message": "Scrolled up"}

        if intent in ["scroll down", "scrolldown"]:
            pyautogui.scroll(-500)
            return {"status": "success", "message": "Scrolled down"}

        # 7. Lock PC & Sleep (Security)
        if intent in ["lock", "lock screen", "lock workstation"]:
            speech_engine.speak("Locking terminal for security, Boss.")
            subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
            return {"status": "success", "message": "Workstation locked"}

        # 8. Clean & Flush RAM
        if intent in ["clean", "boost", "ram", "optimize"]:
            cleaned, before, after = SystemGuard.purge_memory()
            speech_engine.speak("Memory buffers purged. System stabilized, Boss.")
            return {"status": "success", "message": f"Purged {cleaned} files. RAM: {before}% -> {after}%"}

        # 9. Screenshot Capture
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

        # 10. Stealth Focus (Minimize All)
        if intent in ["stealth", "minimize"]:
            dictation_engine.press_key_combo('win', 'd')
            speech_engine.speak("Stealth mode active. All windows cleared, Boss.")
            return {"status": "success", "message": "Engaged Stealth Mode"}

        # 11. Empty Recycle Bin
        if intent in ["empty bin", "clean trash", "empty trash"]:
            try:
                subprocess.run(
                    ["powershell", "-NoProfile", "-Command", "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"],
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                speech_engine.speak("Recycle bin emptied, Boss.")
                return {"status": "success", "message": "Recycle bin emptied safely"}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        # 12. Smart Calculator (OpenInterpreter)
        if intent in ["calc", "calculate", "math"]:
            try:
                result = safe_math_eval(payload)
                speech_engine.speak(f"The answer is {result}, Boss.")
                return {"status": "success", "message": f"{payload} = {result}"}
            except Exception as e:
                return {"status": "error", "message": f"Calculation error: {e}"}

        # 13. Wikipedia Instant Brief (leon-ai / OpenInterpreter)
        if intent in ["wiki", "who is", "what is", "wikipedia"]:
            query = payload or intent
            try:
                encoded = urllib.parse.quote(query)
                req = urllib.request.Request(
                    f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}",
                    headers={'User-Agent': 'JarvisLibertyOS/2.0 (Boss Ahmed edition)'}
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    extract = data.get('extract', '')
                    if extract:
                        short_brief = extract.split('.')[0] + '.'
                        speech_engine.speak(f"Intel on {query}: {short_brief}")
                        return {"status": "success", "message": extract[:280] + "..."}
            except Exception:
                pass
            url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
            webbrowser.open(url)
            return {"status": "success", "message": f"Browsing intel for: {query}"}

        # 14. Weather Brief
        if intent in ["weather", "forecast"]:
            city = payload.strip() or "Delhi"
            try:
                url = f"https://wttr.in/{urllib.parse.quote(city)}?format=%C+%t+%w"
                req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
                with urllib.request.urlopen(req, timeout=4) as resp:
                    weather_text = resp.read().decode('utf-8').strip()
                    speech_engine.speak(f"Weather in {city}: {weather_text}")
                    return {"status": "success", "message": f"Weather in {city}: {weather_text}"}
            except Exception:
                webbrowser.open(f"https://www.google.com/search?q=weather+{urllib.parse.quote_plus(city)}")
                return {"status": "success", "message": f"Looking up weather for {city}"}

        # 15. System Specs & Telemetry Report
        if intent in ["specs", "system", "ip", "specs check"]:
            try:
                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)
                speech_engine.speak(f"System IP is {ip}. All aerospace telemetry nominal, Boss.")
                return {"status": "success", "message": f"Host: {hostname} │ IP: {ip} │ Architecture: 64-bit"}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        # 16. Tactical Humor & Easter Eggs
        if intent in ["joke", "funny"]:
            import random
            joke = random.choice(TECH_JOKES)
            speech_engine.speak(joke)
            return {"status": "success", "message": joke}

        # 17. High-Energy Motivation
        if intent in ["motivate", "motivation", "boost"]:
            msg = speech_engine.get_random_motivation()
            speech_engine.speak(msg)
            return {"status": "success", "message": msg}

        # 18. Timestamp
        if intent in ["time", "date"]:
            now = datetime.datetime.now().strftime("%A, %I:%M %p")
            speech_engine.speak(f"It is {now}, Boss.")
            return {"status": "success", "message": f"Current Time: {now}"}

        # Fallback Query
        url = f"https://www.google.com/search?q={urllib.parse.quote_plus(intent)}"
        webbrowser.open(url)
        speech_engine.speak(f"Looking up {intent}, Boss.")
        return {"status": "success", "message": f"Routed query: {intent}"}
