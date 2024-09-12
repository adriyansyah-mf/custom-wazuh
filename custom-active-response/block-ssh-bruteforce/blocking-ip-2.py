#!/usr/bin/python3
import sys
import json
import os
import datetime
from pathlib import PureWindowsPath, PurePosixPath


if os.name == 'nt':
    LOG_FILE = "C:\\Program Files (x86)\\ossec-agent\\active-response\\active-responses.log"
else:
    LOG_FILE = "/var/ossec/logs/active-responses.log"

PATH_HOSTS_DENY = "/etc/hosts.deny"
def write_debug_file(ar_name, msg):
    with open(LOG_FILE, mode="a") as log_file:
        ar_name_posix = str(PurePosixPath(PureWindowsPath(ar_name[ar_name.find("active-response"):])))
        log_file.write(str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + ar_name_posix + ": " + msg +"\n")

def main(argv):

    write_debug_file(argv[0], "Starting Engine")
    input_str = ""
    for line in sys.stdin:
        input_str = line
        break

    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)

    srcip = data.get('parameters', {}).get('alert', {}).get('data', {}).get('srcip')

    with open(PATH_HOSTS_DENY, "r") as f:
        for line in f:
            if line.strip().startswith(f"sshd: {srcip}"):
                exit()

    with open("", "a") as f:
        f.write(f"sshd: {srcip}\n")



if __name__ == "__main__":
    main(sys.argv)
