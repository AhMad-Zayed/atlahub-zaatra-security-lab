# Direct VPN network access — 2026-11-09

This optional Horizon-only configuration supersedes the original loopback-only access for the vulnerable service. The base Compose and the Windows lab remain unchanged. Mitigated and patched services remain loopback-only.

- Server: 192.168.151.5, ens160.
- Kali: VPN source 10.212.134.201, confirmed by server-side capture of the user's TCP connection. Its earlier 172.18.130.167 address was NATed through Windows and could not be distinguished.
- Allowed network: **10.212.134.0/24**, confirmed by the user's Kali `vpn0` address 10.212.134.201/24 and kernel route to 10.212.134.0/24. User authorized access for every VPN client rather than a single device. This establishes the interface subnet, not the VPN administrator's exact DHCP/address-pool allocation.
- Windows: VPN source 10.212.134.200; direct HTTP 200 verified after broadening the rule.
- Direct URL from any reachable client in the allowed VPN subnet: http://192.168.151.5:28088/
- Loopback mapping 127.0.0.1:28088 is retained for host administration and existing SSH tunnels.

Only the exact private interface is published. The raw PREROUTING hook filters this exact destination IP/TCP port before Docker DNAT; source 10.212.134.0/24 returns to normal Docker filtering, every other inbound source is dropped. This protects both forwarded Docker traffic and any userland-proxy input path. No Docker-owned chain was altered. See https://docs.docker.com/engine/network/packet-filtering-firewalls/ .

The idempotent `/opt/atlahub-zaatra-university/kali-firewall.sh` does not flush existing rules. `atlahub-kali-firewall.service` is enabled and ordered before docker.service so filtering is installed before Docker starts. Boot/restart testing was not performed to avoid disturbing other workloads. The original containers use restart=no; manually start the lab with the override when needed.

Start from the server directory:

```sh
cd /opt/atlahub-zaatra-university
systemctl start atlahub-kali-firewall.service
docker compose -f compose.yaml -f compose.kali.yaml up -d --no-build --pull never
```

Snapshot before changes: `/opt/atlahub-zaatra-university/backups/access-20261108T230435Z/`, containing original Compose, resolved Compose, IPv4/IPv6 firewall snapshots, routes and host application checksums. The UTC timestamp is the preceding calendar day relative to Asia/Hebron.

Initial device-only validation: Windows was blocked with DROP counters increasing; Kali Firefox returned HTTP 200 for the homepage and assets. That Windows restriction is now superseded by the user's request for network-wide VPN access.

Current subnet validation: three containers remain healthy, bindings unchanged, Windows direct HTTP 200, and host Apache/site checksums unchanged. Inspected firewall has exactly the subnet RETURN rule followed by DROP. See `VPN-NETWORK-VALIDATION.txt`. No independent source outside the subnet was available for a new end-to-end negative test, and no source-spoofing or reboot tests were performed. Subnet-change backup: `/opt/atlahub-zaatra-university/backups/vpn-network-20261108T232120Z/`.

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

Every source in 10.212.134.0/24 is now allowed as requested, including newly assigned VPN clients. Addresses outside that subnet remain blocked; connecting a different VPN subnet will require an explicit update. VPN authentication and source-spoofing resistance depend on the VPN's controls. Legacy filenames retain "kali" for operational continuity but enforce the network-wide rule above.
