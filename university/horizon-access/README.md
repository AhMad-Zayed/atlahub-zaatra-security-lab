# Restricted direct Kali access — 2026-11-09

This optional Horizon-only configuration supersedes the original loopback-only access for the vulnerable service. The base Compose and the Windows lab remain unchanged. Mitigated and patched services remain loopback-only.

- Server: 192.168.151.5, ens160.
- Kali: VPN source 10.212.134.201, confirmed by server-side capture of the user's TCP connection. Its earlier 172.18.130.167 address was NATed through Windows and could not be distinguished.
- Windows: VPN source 10.212.134.200; explicitly tested and blocked.
- Direct URL from Kali: http://192.168.151.5:28088/
- Loopback mapping 127.0.0.1:28088 is retained for host administration and existing SSH tunnels.

Only the exact private interface is published. The raw PREROUTING hook filters this exact destination IP/TCP port before Docker DNAT; source 10.212.134.201/32 returns to normal Docker filtering, every other inbound source is dropped. This protects both forwarded Docker traffic and any userland-proxy input path. No Docker-owned chain was altered. See https://docs.docker.com/engine/network/packet-filtering-firewalls/ .

The idempotent `/opt/atlahub-zaatra-university/kali-firewall.sh` does not flush existing rules. `atlahub-kali-firewall.service` is enabled and ordered before docker.service so filtering is installed before Docker starts. Boot/restart testing was not performed to avoid disturbing other workloads. The original containers use restart=no; manually start the lab with the override when needed.

Start from the server directory:

```sh
cd /opt/atlahub-zaatra-university
systemctl start atlahub-kali-firewall.service
docker compose -f compose.yaml -f compose.kali.yaml up -d --no-build --pull never
```

Snapshot before changes: `/opt/atlahub-zaatra-university/backups/access-20261108T230435Z/`, containing original Compose, resolved Compose, IPv4/IPv6 firewall snapshots, routes and host application checksums. The UTC timestamp is the preceding calendar day relative to Asia/Hebron.

Verified after changes: three containers healthy; target loopback HTTP 200; only 127.0.0.1 and 192.168.151.5 bindings on target; Windows connection times out with DROP counters increasing; host Apache/site file checksums unchanged. Server access logs subsequently recorded direct Firefox/Linux requests from Kali 10.212.134.201, including successful HTTP 200 responses for the site assets with referer http://192.168.151.5:28088/. The allow-rule counter increased to 648 packets; the block-rule counter recorded the three Windows test packets. No source-spoofing tests were performed.

## Rollback

First remove the private publication by applying base Compose alone. Confirm only loopback remains, then remove the dedicated firewall hook and disable its boot service:

```sh
cd /opt/atlahub-zaatra-university
docker compose -f compose.yaml up -d --no-build --pull never --no-deps vulnerable
ss -lnt | grep 28088
# Continue only after confirming 192.168.151.5:28088 is absent:
systemctl disable --now atlahub-kali-firewall.service
iptables -w -t raw -D PREROUTING -d 192.168.151.5/32 -p tcp --dport 28088 -j ATLAHUB-KALI
iptables -w -t raw -F ATLAHUB-KALI
iptables -w -t raw -X ATLAHUB-KALI
```

Do not restore the entire iptables snapshot blindly, because Docker's container-specific rules may have changed. Do not flush global firewall chains. Configuration files are retained for audit and reuse.

The allowlist identifies a VPN IP, not a permanent device identity. If the VPN reassigns 10.212.134.201 to another client, that client would inherit access. Keep this address reserved for Kali or roll back the publication when the lab ends. A changed Kali VPN address is blocked until explicitly revalidated and updated. Broader firewall/source-spoofing resistance depends on the VPN's controls.
