#!/usr/bin/python3
import sys
import json
import os
import subprocess
import datetime
from pathlib import PureWindowsPath, PurePosixPath


if os.name == 'nt':
    LOG_FILE = "C:\\Program Files (x86)\\ossec-agent\\active-response\\active-responses.log"
else:
    LOG_FILE = "/var/ossec/logs/active-responses.log"

def write_debug_file(ar_name, msg):
    with open(LOG_FILE, mode="a") as log_file:
        ar_name_posix = str(PurePosixPath(PureWindowsPath(ar_name[ar_name.find("active-response"):])))
        log_file.write(str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + ar_name_posix + ": " + msg +"\n")

def main(argv):

    write_debug_file(argv[0], "Starting Engine")
    input_str = ""
    for line in sys.stdin:
        input_str += line

    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)

    srcip = data.get('parameters', {}).get('alert', {}).get('data', {}).get('srcip')
    with open("/etc/hosts.deny", "a") as f:
        f.write(f"sshd: {srcip}")



if __name__ == "__main__":
    main(sys.argv)
