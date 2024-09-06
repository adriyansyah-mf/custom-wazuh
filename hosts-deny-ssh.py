#!/usr/bin/env python3
import json
import os
import time

# Set paths and constants
HOSTS_DENY_FILE = "/etc/hosts.deny"
LOG_FILE = "logs/ssh-brute-force.log"
BAN_TIME = 600  # 10 minutes ban time
FAIL_THRESHOLD = 3  # Number of failed attempts before banning

# Read input JSON from stdin
input_json = json.loads(input())

# Extract parameters
username = input_json["username"]
ip = input_json["src_ip"]

# Function to log to file
def log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")

# Function to block IP using hosts.deny
def block_ip(ip_address):
    with open(HOSTS_DENY_FILE, "a") as hosts_deny:
        hosts_deny.write(f"sshd: {ip_address}\n")
    log(f"SSH brute force detected from {ip_address}. IP blocked in hosts.deny for {BAN_TIME} seconds.")

# Function to check SSH brute force attempts
def check_ssh_brute_force(username, ip_address):
    # Placeholder function for checking brute force attempts
    # For demo purposes, always return True (simulating brute force attempt)
    return True

# Main function
def main():
    # Check for SSH brute force attempts
    if check_ssh_brute_force(username, ip):
        log(f"SSH brute force attempt detected from {ip} for user {username}.")

        # Count failed attempts from IP in last 10 minutes
        with open(LOG_FILE, "r") as log_file:
            lines = log_file.readlines()
            recent_attempts = 0
            current_time = time.time()

            for line in reversed(lines):
                log_time, log_message = line.strip().split(" ", 1)
                log_timestamp = float(log_time)
                if current_time - log_timestamp > BAN_TIME:
                    break  # Stop checking if logs are older than ban time

                if f"SSH brute force attempt detected from {ip} for user {username}." in log_message:
                    recent_attempts += 1
                    if recent_attempts >= FAIL_THRESHOLD:
                        block_ip(ip)
                        break

        # Log the attempt
        log(f"{time.time()} SSH brute force attempt detected from {ip} for user {username}.")

if __name__ == "__main__":
    main()
