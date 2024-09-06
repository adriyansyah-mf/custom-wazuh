#!/var/ossec/framework/python/bin/python3

import os
import sys
import json
import datetime
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Determine paths based on OS
if os.name == 'nt':
    LOG_FILE = "C:\\Program Files (x86)\\ossec-agent\\active-response\\active-responses.log"
else:
    LOG_FILE = "/var/ossec/logs/active-responses.log"

HOSTS_FILE = '/etc/hosts.deny'  # Path to hosts.deny file

def blocked_ip(argv):
    """Blocked IP active response for Wazuh."""
    try:
        data = json.loads(argv)
        ip = data['parameters']['alert']['data']['srcip']

        # Append IP to hosts.deny file
        with open(HOSTS_FILE, 'a') as f:
            f.write(f"sshd: {ip}\n")
            logger.info(f"Added {ip} to {HOSTS_FILE}")

        # Log the IP that will be blocked
        with open(LOG_FILE, 'a') as l:
            l.write(logger.info(f"Blocking IP: {ip}"))
        
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {str(e)}")
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <json_data>")
        sys.exit(1)

    blocked_ip(sys.argv)
