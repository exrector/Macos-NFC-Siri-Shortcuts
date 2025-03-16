# Macos-NFC-Siri-Shortcuts

Проект предназначен для запуска  siri shortcuts на компьютерах MACOS с помощью NFC tags!

The project is designed to run siri shortcuts automations on MACOS computers using NFC tags!

The project used: 
- ACS ACR1552U USB-C NFC Reader IV
- NTAG213 Chip 144 Bytes Memory
- optional case
  
Я преследовал целью использовать один тег дважды - двойной проход (это условие моего проекта)

1. pip install pyscard
2.  Create Siri Shortcuts
- Create two shortcuts named **SHORTCUT_A** and **SHORTCUT_B** in the Shortcuts app.
4. Key Changes:
1. **Per-UID Limits**: Each UID can only trigger twice
2. **Continuous Operation**: Script keeps running indefinitely, only blocking UIDs that have reached their 2-trigger limit
3. **Independent Counters**: Track triggers separately for each UID

### Behavior:
| Scan Count | UID 1 (04:01:02:AA:83:6B:85) | UID 2 (04:00:03:AA:83:6B:85) |
|------------|-------------------------------|-------------------------------|
| 1st Scan   | Runs SHORTCUT_A               | Runs SHORTCUT_C               |
| 2nd Scan   | Runs SHORTCUT_B               | Runs SHORTCUT_D               |
| 3rd+ Scan  | Ignored                       | Ignored                       |

### Features:
- Will continue monitoring for new tags (you can add more UIDs to `TARGET_UIDS`)
- Shows remaining triggers for each UID (`1/2` or `2/2`)
- 3-second cooldown prevents accidental duplicate scans
- Clean error handling for card removal/reader issues

To exit the script, press `Ctrl+C` in Terminal. Add more UIDs to the `TARGET_UIDS` dictionary to support additional tags and shortcuts.
