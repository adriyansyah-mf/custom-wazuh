#!/usr/bin/python3
import sys
import json
import os
import datetime
from pathlib import PureWindowsPath, PurePosixPath

APACHE_PATH = "/var/www/html/"
if os.name == 'nt':
    LOG_FILE = "C:\\Program Files (x86)\\ossec-agent\\active-response\\active-responses.log"
else:
    LOG_FILE = "/var/ossec/logs/active-responses.log"

def write_debug_file(ar_name, msg):
    with open(LOG_FILE, mode="a") as log_file:
        ar_name_posix = str(PurePosixPath(PureWindowsPath(ar_name[ar_name.find("active-response"):])))
        log_file.write(str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + ar_name_posix + ": " + msg +"\n")



def get_all_folders(path):
    """Get All in a path

    Args:
        path (str): path
    """
    folders = []
    for entry in os.scandir(path):
        if entry.is_dir():
            folders.append(entry.name)
    return folders

def main(argv):

    write_debug_file(argv[0], "Defend Apache2")
    input_str = ""
    for line in sys.stdin:
        input_str = line
        break
    
    target_folders = get_all_folders(APACHE_PATH)
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)

    srcip = data.get('parameters', {}).get('alert', {}).get('data', {}).get('srcip')
    for folder in target_folders:
        htaccess_path = os.path.join(APACHE_PATH, folder, ".htaccess")
        if os.path.exists(htaccess_path):
            mode = "a"  # Append mode if .htaccess already exists
        else:
            mode = "w"  # Create new .htaccess file if it doesn't exist
        
        # Write redirect rule to .htaccess file
        with open(htaccess_path, mode) as htaccess_file:
            htaccess_file.write(f"\n# Redirect {srcip} to Google\n")
            htaccess_file.write(f"RewriteEngine On\n")
            htaccess_file.write("RewriteCond"+" "+"%{REMOTE_ADDR}"+f"^{srcip}$\n")
            htaccess_file.write(f"RewriteRule ^(.*)$ https://google.com [L,R=301]\n")


            print(f"Updated .htaccess in {os.path.join(APACHE_PATH, folder)} for {srcip}")




if __name__ == "__main__":
    main(sys.argv)
