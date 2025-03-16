import time
from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
import subprocess

# Mapping of UIDs to Siri Shortcut sequences
TARGETS = {
    "04:01:02:AA:83:6B:85": ["SHORTCUT_A", "SHORTCUT_B"],
    "04:00:03:AA:83:6B:85": ["SHORTCUT_C", "SHORTCUT_D"],
    "04:01:06:AA:83:6B:85": ["SHORTCUT_E", "SHORTCUT_F"]
}

TRACKER = {}  # Tracks current shortcut index for each UID

def get_uid(connection):
    GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
    response, sw1, sw2 = connection.transmit(GET_UID)
    if sw1 == 0x90 and sw2 == 0x00:
        return response
    return None

def format_uid(uid_bytes):
    return ":".join(f"{byte:02X}" for byte in uid_bytes)

def run_shortcut(uid_str):
    if uid_str in TARGETS:
        shortcuts = TARGETS[uid_str]
        current_idx = TRACKER.get(uid_str, 0)
        
        # Run the current shortcut
        shortcut = shortcuts[current_idx]
        print(f"Running {shortcut} for UID {uid_str}")
        subprocess.run(["shortcuts", "run", shortcut])
        
        # Update index for next scan
        TRACKER[uid_str] = (current_idx + 1) % len(shortcuts)

def monitor_nfc():
    reader = readers()[0]
    print(f"Monitoring reader: {reader}")

    while True:
        try:
            conn = reader.createConnection()
            conn.connect()

            uid_bytes = get_uid(conn)
            if uid_bytes:
                uid_str = format_uid(uid_bytes)
                run_shortcut(uid_str)

            # Wait for tag removal
            while True:
                time.sleep(0.1)
                conn.disconnect()
                conn.connect()

        except (NoCardException, CardConnectionException):
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    monitor_nfc()