#!/usr/bin/python3
import sys
import json
import subprocess
import datetime

LOG_FILE = "/var/ossec/logs/active-responses.log"

def write_to_log(message):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, mode='a') as log_file:
        log_file.write(f"{current_time} - {message}\n")

def main():
    # Membaca input JSON dari stdin
    input_str = sys.stdin.read()
    write_to_log(f"Received input JSON: {input_str}")
    print(input_str)
    try:
        data = json.loads(input_str)
    except ValueError:
        error_message = "Error: Invalid JSON input"
        print(error_message)
        write_to_log(error_message)
        sys.exit(1)
    
    # Ambil informasi alert yang diperlukan
    alert = data.get("parameters", {}).get("alert", {})
    if not alert:
        error_message = "Error: No alert data found in JSON input"
        print(error_message)
        write_to_log(error_message)
        sys.exit(1)
    
    # Ambil informasi yang Anda perlukan dari alert (misalnya, alamat IP sumber)
    source_ip = alert.get("data", {}).get("srcip")
    if not source_ip:
        error_message = "Error: No source IP found in alert data"
        print(error_message)
        write_to_log(error_message)
        sys.exit(1)
    
    # Contoh tindakan: menambahkan aturan firewall untuk menolak lalu lintas dari alamat IP tertentu ke port SSH (22)
    command = f"iptables -A INPUT -s {source_ip} -p tcp --dport ssh -j DROP"
    
    # Eksekusi perintah
    try:
        subprocess.run(command, shell=True, check=True)
        success_message = f"Blocked traffic from {source_ip} to SSH port"
        print(success_message)
        write_to_log(success_message)
    except subprocess.CalledProcessError as e:
        error_message = f"Error: Command execution failed: {e}"
        print(error_message)
        write_to_log(error_message)
        sys.exit(1)

if __name__ == "__main__":
    main()
