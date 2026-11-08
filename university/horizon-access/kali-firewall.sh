#!/bin/sh
set -eu
# Filter original destination before Docker DNAT. Only the Kali VPN /32 is allowed.
iptables -w -t raw -N ATLAHUB-KALI 2>/dev/null || true
iptables -w -t raw -C ATLAHUB-KALI -j DROP 2>/dev/null || iptables -w -t raw -A ATLAHUB-KALI -j DROP
iptables -w -t raw -C ATLAHUB-KALI -s 10.212.134.201/32 -j RETURN 2>/dev/null || iptables -w -t raw -I ATLAHUB-KALI 1 -s 10.212.134.201/32 -j RETURN
iptables -w -t raw -C PREROUTING -d 192.168.151.5/32 -p tcp --dport 28088 -j ATLAHUB-KALI 2>/dev/null || iptables -w -t raw -I PREROUTING 1 -d 192.168.151.5/32 -p tcp --dport 28088 -j ATLAHUB-KALI
