# Persistence Toolkit

> Persistence Mechanism Research & Implementation for Red Teams

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-red)

## Overview

A comprehensive toolkit covering Windows and Linux persistence mechanisms used by advanced threat actors. Built for authorized red team simulations and adversary emulation exercises.

## Techniques

- Registry-based persistence (Run keys, COM hijacking)
- Scheduled tasks & cron job persistence
- Service installation & DLL hijacking
- Boot/pre-OS persistence techniques
- WMI event subscriptions
- Linux systemd & init.d persistence

## Quick Start

```bash
git clone https://github.com/Youssefzdb/persistence-toolkit
cd persistence-toolkit
pip install -r requirements.txt
python persist.py --method registry --payload shell.exe
```

## MITRE ATT&CK Coverage

- T1547 - Boot or Logon Autostart Execution
- T1053 - Scheduled Task/Job
- T1543 - Create or Modify System Process
- T1546 - Event Triggered Execution

## Legal Disclaimer

> For authorized red team operations and lab environments only.

## Author

**Youssef Zeidi** | Red Team Specialist | [GitHub](https://github.com/Youssefzdb)
