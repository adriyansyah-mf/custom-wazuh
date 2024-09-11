# Block an IP FROM ACCES A URL

# COMMAND IP TABLES

```bash
iptables -t nat -A PREROUTING -s ATTACKER_IP -p tcp --dport 80 -j DNAT --to-destination your-server-ip:80
iptables -t nat -A POSTROUTING -j MASQUERADE
```