import os
import sys


@staticmethod
def detection_os():
    """Detection Operation System

    Returns:
        _str_: Windows|Linux
    """
    if os.name == 'nt':
        return 'Windows'
    else:
        return 'Linux'

@staticmethod
def write_log():
    """Writing Log Of Active Response
    """
    if detection_os is 'Windows':
        return 

def block_traffic(ip_address):
    """Function To Block Traffic

    Args:
        ip_address (_type_): Attacked IP Address
        port (_type_): Destination Port
    """


    host_deny_path = '/etc/hosts.deny'
    try:
        with open(host_deny_path, "a") as f:
            f.write(f"sshd: {ip_address}")

        print(f"Blocked {ip_address} to access SSH")
    except Exception as e:
        print(f"Unknown Error {str(e)}")


if __name__ == '__main__':
    """
    Calling Main Function
    """
    if len(sys.argv) != 4:
        print("Usage: Python3 firewall-drop-specific.py ip")
        sys.exit()


    ip_address = sys.argv[1]

    block_traffic(ip_address)