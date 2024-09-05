import os
import sys


def block_traffic(ip_address):
    """Function To Block Traffic

    Args:
        ip_address (str): Attacked IP Address
    """
    host_deny_path = '/etc/hosts.deny'
    try:
        with open(host_deny_path, "a") as f:
            f.write(f"sshd: {ip_address}\n")  # Add a newline to ensure proper formatting

        print(f"Blocked {ip_address} to access SSH")
    except Exception as e:
        print(f"Unknown Error: {str(e)}")


if __name__ == '__main__':
    """
    Main function to block IP address passed as argument
    """
    if len(sys.argv) != 2:
        print("Usage: python3 firewall-drop-specific.py <ip_address>")
        sys.exit()

    ip_address = sys.argv[1]

    block_traffic(ip_address)
