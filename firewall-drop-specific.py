#!/var/ossec/python/bin/python3

import os
import sys

def block_traffic(ip_address, port):
    """Function To Block Traffic

    Args:
        ip_address (str): Attacked IP Address
        port (str): Port number to block (e.g., "22" for SSH)
    """
    try:
        iptables_cmd = f"iptables -A INPUT -s {ip_address} -p tcp --dport {port} -j DROP"
        
        os.system(iptables_cmd)
        
        print(f"Blocked {ip_address} from accessing port {port}")
    except Exception as e:
        print(f"Unknown Error: {str(e)}")

if __name__ == '__main__':
    """
    Main function to block IP address passed as argument
    """
    if len(sys.argv) != 3:
        print("Usage: python3 firewall-drop-specific.py <ip_address> <port>")
        sys.exit()

    ip_address = sys.argv[1]
    port = sys.argv[2]

    block_traffic(ip_address, port)
