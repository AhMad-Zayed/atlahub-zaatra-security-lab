#!/bin/sh
set -eu
# VPN interface network confirmed by Kali: 10.212.134.201/24 and its kernel route.
# Filter only the private target TCP port before Docker DNAT.
iptables -w -t raw -N ATLAHUB-KALI 2>/dev/null || true
iptables -w -t raw -C ATLAHUB-KALI -j DROP 2>/dev/null || iptables -w -t raw -A ATLAHUB-KALI -j DROP
iptables -w -t raw -C ATLAHUB-KALI -s 10.212.134.0/24 -j RETURN 2>/dev/null || iptables -w -t raw -I ATLAHUB-KALI 1 -s 10.212.134.0/24 -j RETURN
iptables -w -t raw -C PREROUTING -d 192.168.151.5/32 -p tcp --dport 28088 -j ATLAHUB-KALI 2>/dev/null || iptables -w -t raw -I PREROUTING 1 -d 192.168.151.5/32 -p tcp --dport 28088 -j ATLAHUB-KALI
# Remove the superseded per-device rules without flushing the active chain.
for address in 10.212.134.200/32 10.212.134.201/32; do
  if iptables -w -t raw -C ATLAHUB-KALI -s "$address" -j RETURN 2>/dev/null; then
    iptables -w -t raw -D ATLAHUB-KALI -s "$address" -j RETURN
  fi
done
