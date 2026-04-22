import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random

users = {
    "alice": "Alice@123",
    "bob": "Bob@123",
    "admin": "Admin@123",
    "john": "John@123"
}

attack_log = []
locked = False
risk_score = 0


def log_event(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_box.insert(tk.END, f"[{timestamp}] {message}\n")
    log_box.see(tk.END)


def start_attack():
    global risk_score
    common_password = password_entry.get()

    if not common_password:
        log_event("Enter attack password first.")
        return

    failed_count = 0

    log_event("Password spraying attack started...")

    for username in users:
        if users[username] == common_password:
            log_event(f"[SUCCESS] Account compromised: {username}")
        else:
            log_event(f"[FAILED] Login failed for {username}")
            failed_count += 1

    risk_score = failed_count * 20
    risk_label.config(text=f"Risk Score: {risk_score}")

    if risk_score >= 60:
        detect_attack()


def detect_attack():
    log_event("Suspicious behavior detected!")
    log_event("Multiple accounts targeted with same password.")
    lockout()


def lockout():
    global locked
    locked = True
    status_label.config(text="Status: ATTACK BLOCKED")
    log_event("Source temporarily locked for 30 seconds.")
    root.after(30000, unlock_system)


def unlock_system():
    global locked
    locked = False
    status_label.config(text="Status: System Active")
    log_event("Lockout expired. System active again.")


def reset_logs():
    log_box.delete(1.0, tk.END)
    risk_label.config(text="Risk Score: 0")
    status_label.config(text="Status: System Active")


root = tk.Tk()
root.title("Password Spraying Attack Simulator")
root.geometry("700x500")

title = tk.Label(root, text="Password Spraying Attack vs Smart Lockout Defense",
                 font=("Arial", 14, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Common Password Used by Attacker:").grid(row=0, column=0, padx=5)
password_entry = tk.Entry(frame, width=25)
password_entry.grid(row=0, column=1)

attack_btn = tk.Button(root, text="Start Attack Simulation", command=start_attack)
attack_btn.pack(pady=5)

reset_btn = tk.Button(root, text="Reset", command=reset_logs)
reset_btn.pack(pady=5)

risk_label = tk.Label(root, text="Risk Score: 0", font=("Arial", 12))
risk_label.pack()

status_label = tk.Label(root, text="Status: System Active", font=("Arial", 12))
status_label.pack()

log_box = tk.Text(root, height=15, width=80)
log_box.pack(pady=10)

root.mainloop()