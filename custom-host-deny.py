#!/usr/bin/python3

import os
import sys
import re
import time

HOSTS_DENY_FILE = "/etc/hosts.deny"
HOSTS_ALLOW_FILE = "/etc/hosts.allow"
LOCK_FILE = "/var/lock/host-deny-lock"

MAX_ITERATION = 50

def lock():
    i = 0
    while True:
        try:
            lock_fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(lock_fd, str(os.getpid()).encode())
            os.close(lock_fd)
            return
        except FileExistsError:
            try:
                with open(LOCK_FILE, 'r') as lock_file:
                    locked_pid = int(lock_file.read().strip())
                if locked_pid == os.getpid():
                    return
                else:
                    i += 1
            except FileNotFoundError:
                pass
        if i >= MAX_ITERATION:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} Unable to execute. Locked: {sys.argv[0]}")
            unlock()
            sys.exit(1)
        time.sleep(i)


def unlock():
    try:
        os.remove(LOCK_FILE)
    except FileNotFoundError:
        pass


def add_ip_to_hosts_deny(ip):
    if re.match(r'^[a-fA-F0-9\.:]+$', ip):
        ip = f"[{ip}]"
    
    with open(HOSTS_DENY_FILE, 'a') as f:
        f.write(f"sshd: {ip}\n")


def delete_ip_from_hosts_deny(ip):
    if re.match(r'^[a-fA-F0-9\.:]+$', ip):
        ip = f"
\[{ip}\]"

    try:
        with open(HOSTS_DENY_FILE, 'r') as f:
            lines = f.readlines()
        
        with open(HOSTS_DENY_FILE, 'w') as f:
            for line in lines:
                if f"sshd: {ip}" not in line:
                    f.write(line)
    except FileNotFoundError:
        pass


def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <action> <user> <ip>")
        sys.exit(1)
    
    action = sys.argv[1]
    user = sys.argv[2]
    ip = sys.argv[3]

    if action == "add":
        lock()
        add_ip_to_hosts_deny(ip)
        unlock()
    elif action == "delete":
        lock()
        delete_ip_from_hosts_deny(ip)
        unlock()
    else:
        print(f"{sys.argv[0]}: invalid action: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
