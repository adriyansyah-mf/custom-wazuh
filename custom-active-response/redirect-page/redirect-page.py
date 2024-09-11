#!/usr/bin/python3
import sys
import json
import os
import datetime
import subprocess
from pathlib import PureWindowsPath, PurePosixPath


DESTINATION = "20.200.102.2"

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
        break

    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)
    srcip = data.get('parameters', {}).get('alert', {}).get('data', {}).get('srcip')
    if '.' in srcip:
        try:
            
            cmd = f"iptables -t nat -A PREROUTING -s {srcip} -p tcp --dport 80 -j DNAT --to-destination {DESTINATION}:80\n"
            cmd2 = f"iptables -t nat -A PREROUTING -s {srcip} -p tcp --dport 443 -j DNAT --to-destination {DESTINATION}:443\n"
            cmd3 = f"iptables -t nat -A POSTROUTING -j MASQUERADE"
            subprocess.run(cmd, shell=True, check=True)
            subprocess.run(cmd2, shell=True, check=True)
            subprocess.run(cmd3, shell=True, check=True)
            write_debug_file(argv[0], f"Redirect IP {srcip}")
        except subprocess.CalledProcessError as e:
            write_debug_file(argv[0], str(e))
        except Exception as e:
            write_debug_file(argv[0], str(e))
    elif ':' in srcip:
        try:
            
            cmd = f"ip6tables -t nat -A PREROUTING -s {srcip} -p tcp --dport 80 -j DNAT --to-destination {DESTINATION}:80\n"
            cmd2 = f"ip6tables -t nat -A PREROUTING -s {srcip} -p tcp --dport 443 -j DNAT --to-destination {DESTINATION}:443\n"
            cmd3 = f"iptables -t nat -A POSTROUTING -j MASQUERADE"
            subprocess.run(cmd, shell=True, check=True)
            subprocess.run(cmd2, shell=True, check=True)
            subprocess.run(cmd3, shell=True, check=True)
            write_debug_file(argv[0], f"Redirect IP {srcip}")
        except subprocess.CalledProcessError as e:
            write_debug_file(argv[0], str(e))
        except Exception as e:
            write_debug_file(argv[0], str(e))

    print("Execution Success\n")

if __name__ == "__main__":
    main(sys.argv)
