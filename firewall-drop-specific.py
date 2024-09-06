import subprocess
import sys
import logging

# Setup logging
logging.basicConfig(
    filename="/var/log/block_ip.log",  # Sesuaikan path file log
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def block_ip(ip, port):
    try:
        # Command untuk menambahkan rule iptables yang memblokir IP pada port tertentu
        command = f"iptables -I INPUT -s {ip} -p tcp --dport {port} -j DROP"
        
        # Eksekusi perintah menggunakan subprocess
        subprocess.run(command, shell=True, check=True)
        
        # Log keberhasilan
        logging.info(f"IP {ip} berhasil diblokir pada port {port}")
        print(f"IP {ip} berhasil diblokir pada port {port}")
    except subprocess.CalledProcessError as e:
        # Log kegagalan
        logging.error(f"Gagal memblokir IP {ip} pada port {port}: {e}")
        print(f"Gagal memblokir IP {ip} pada port {port}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: block_ip.py <IP> <PORT>")
        sys.exit(1)

    ip_address = sys.argv[1]
    port_number = sys.argv[2]
    
    block_ip(ip_address, port_number)
