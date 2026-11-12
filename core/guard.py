"""
J.A.R.V.I.S. Liberty // System Guardian & Zero-Damage Guardrail
Protects laptop hardware, prevents accidental destructive actions,
and purges junk memory buffers safely.
"""

import os
import gc
import psutil
from typing import Tuple

PROTECTED_PATHS = [
    "c:\\windows",
    "c:\\program files",
    "c:\\program files (x86)",
    "system32"
]

class SystemGuard:
    @staticmethod
    def validate_action(command: str) -> Tuple[bool, str]:
        """Validates command against destructive operations."""
        cmd_lower = command.lower().strip()
        destructive_patterns = [
            "format ", "rmdir /s /q c:", "del /f /s /q c:\\", "drop database", "vssadmin delete"
        ]
        for pattern in destructive_patterns:
            if pattern in cmd_lower:
                return False, f"Action blocked by Safety Guardian: Destructive sequence detected ({pattern})."

        for p in PROTECTED_PATHS:
            if f"delete {p}" in cmd_lower or f"remove {p}" in cmd_lower:
                return False, f"Action blocked: Path {p} is protected from modifications."

        return True, "Verified safe."

    @staticmethod
    def purge_memory() -> Tuple[int, float, float]:
        """Performs safe garbage collection and frees temporary disk/RAM overhead."""
        ram_before = psutil.virtual_memory().percent
        gc.collect()

        temp_dir = os.environ.get('TEMP', '')
        cleaned_files = 0
        if os.path.exists(temp_dir):
            try:
                for f in os.listdir(temp_dir)[:60]:
                    p = os.path.join(temp_dir, f)
                    if os.path.isfile(p):
                        try:
                            os.remove(p)
                            cleaned_files += 1
                        except Exception:
                            pass
            except Exception:
                pass

        ram_after = psutil.virtual_memory().percent
        return cleaned_files, ram_before, ram_after
