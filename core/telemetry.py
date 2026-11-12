"""
J.A.R.V.I.S. Liberty // System Telemetry & Hardware Sensors
Gathers live metrics for CPU, RAM, Battery, Disk, and Process Load.
"""

import psutil

def get_system_vitals() -> dict:
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('C:\\')
    battery = psutil.sensors_battery()

    batt_pct = battery.percent if battery else 100
    batt_plugged = battery.power_plugged if battery else True
    batt_status = "⚡ Charging" if batt_plugged else "🔋 On Battery"

    return {
        "cpu_percent": cpu,
        "ram_used_gb": round(ram.used / (1024**3), 2),
        "ram_total_gb": round(ram.total / (1024**3), 2),
        "ram_percent": ram.percent,
        "disk_free_gb": round(disk.free / (1024**3), 1),
        "disk_total_gb": round(disk.total / (1024**3), 1),
        "battery_percent": batt_pct,
        "battery_status": batt_status,
        "battery_plugged": batt_plugged
    }
