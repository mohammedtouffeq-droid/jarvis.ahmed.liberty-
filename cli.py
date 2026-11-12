"""
=============================================================================
                  ⚡ J.A.R.V.I.S. LIBERTY // TERMINAL OS ⚡
                       Dedicated to Boss Ahmed
=============================================================================
"""

import os
import sys
import time
from pathlib import Path

# Add root directory to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from core.speech import speech_engine
from core.telemetry import get_system_vitals
from core.controller import dispatcher

console = Console()

BANNER = """
[bold cyan]
      ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
      ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
      ██║███████║██████╔╝██║   ██║██║███████╗
 ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
 ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
[/bold cyan]
[bold white]  TACTICAL DESKTOP OS[/bold white] [bold yellow]v1.0 LIBERTY[/bold yellow]  │  [bold green]OPERATOR: BOSS AHMED[/bold green]
"""

def print_telemetry():
    v = get_system_vitals()
    table = Table(title="[bold cyan]⚡ LIVE TELEMETRY MATRIX[/bold cyan]", border_style="cyan")
    table.add_column("Subsystem", style="bold white", width=18)
    table.add_column("Reading", width=28)
    table.add_column("Status", style="bold green", width=16)

    table.add_row("CPU Load", f"{v['cpu_percent']}% utilized", "HEALTHY")
    table.add_row("Memory (RAM)", f"{v['ram_used_gb']} GB / {v['ram_total_gb']} GB ({v['ram_percent']}%)", "OPTIMAL")
    table.add_row("Power Core", f"{v['battery_percent']}% ({v['battery_status']})", "ACTIVE")
    table.add_row("Storage (C:)", f"{v['disk_free_gb']} GB Free / {v['disk_total_gb']} GB", "NOMINAL")
    console.print(table)

def main():
    os.system("cls" if os.name == "nt" else "clear")
    console.print(BANNER)
    print_telemetry()

    speech_engine.is_armed = True
    boot = speech_engine.get_boot_salute()
    console.print(f"\n[bold yellow]⚡ J.A.R.V.I.S.:[/bold yellow] [white]{boot}[/white]\n")
    speech_engine.speak(boot, force=True)

    console.print("[dim]Type your order (e.g. 'type Hello World', 'open chrome', 'clean', 'snap', 'motivate', 'exit')[/dim]\n")

    while True:
        try:
            cmd = console.input("[bold cyan]J.A.R.V.I.S.[/bold cyan] [bold white]❯[/bold white] ").strip()
            if not cmd:
                continue

            if cmd.lower() in ["exit", "quit", "poweroff", "shutdown"]:
                farewell = "Shutting down auxiliary protocols. Good night, Boss Ahmed."
                console.print(f"[bold yellow]{farewell}[/bold yellow]")
                speech_engine.speak(farewell, force=True)
                time.sleep(1)
                break

            elif cmd.lower() in ["hud", "vitals", "status"]:
                print_telemetry()

            elif cmd.lower() in ["cls", "clear"]:
                os.system("cls" if os.name == "nt" else "clear")
                console.print(BANNER)
                print_telemetry()

            else:
                res = dispatcher.dispatch(cmd)
                status_color = "green" if res.get("status") == "success" else "red"
                console.print(f"[bold {status_color}]{res.get('message', '')}[/bold {status_color}]")

        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Session terminated safely.[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()
