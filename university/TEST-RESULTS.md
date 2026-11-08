# Validation record

Validation date: 2026-11-09, Asia/Hebron. Only actually executed checks are marked PASS. This report is supplemented by `LOCAL-VALIDATION.txt`, `HORIZON-VALIDATION.txt`, `IMAGE-MANIFEST.json` and screenshots.

## Local implementation checks — PASS

- Built three images successfully from the exact original official PHP/Apache digests.
- Ran `validate.py`: 54 non-destructive checks passed across vulnerable, mitigated and patched services. Includes GET/HEAD version headers, attribution, mod_php SAPI, correct variant settings, health, loopback bindings, evidence SHA-256, evidence HTTP 404, locked shell HTTP 403, bundled asset responses and PHP syntax checks.
- Ran `node --check www/assets/zaatra.js`: passed.
- Browser checked desktop at the default approximately 1280-pixel viewport and mobile at 390 × 844. RTL layout fits the viewport without horizontal overflow. All five image elements loaded after viewing the page. Mobile menu expands and closes upon navigation.
- Destination filter: selecting Jordan shows exactly the Petra card. Jordan + city shows the empty state. Reset restores all three cards.
- Selected Petra, two travelers and 2026-12-15: reservation summary displayed a fictional total of $580 and confirmed no booking/data submission.
- Captured desktop, mobile, destinations, booking and attribution screenshots. No error/warning entries were reported by the browser log check.
- Compared 13 existing Windows lab source/configuration files against the initial SHA-256 baseline: zero changed files. Original three containers remained healthy on ports 18088, 8090 and 18089.
- Compared upstream research paths against upstream commit `f0a07a8`: no differences. Original source and research history retained.
- Pushed customization branch `university/zaatra-atlahub` to the authenticated account's GitHub fork.

## Horizon deployment checks — PASS

- Installed Docker Engine 29.9.3 and Docker Compose v5.7.0 on Ubuntu 24.04.5; host Apache remained active.
- Transferred the locally built archive over authenticated SFTP; its SHA-256 matched before loading. No remote application rebuild was performed.
- Verified embedded image config digests, all uncompressed filesystem layer digests and runtime configuration across both image stores for all three services. Displayed Docker image IDs differ because the classic and containerd stores report different identity types; the configuration and layers are identical. See `IMAGE-PARITY.txt` and `IMAGE-MANIFEST.json`.
- Ran `validate.py` on Horizon: all 54 non-destructive acceptance checks passed. All three containers were healthy.
- Ran Nmap service identification and the standard `http-headers` script on the three loopback ports. PHP/8.4.26 was reported on target/mitigated, PHP/8.4.27 on patched. The initial scan without service detection did not run HTTP discovery on these nonstandard ports; rerunning with `-sV --version-light` produced the recorded headers in `NMAP-HEADERS.txt`.
- `ss -lnt` and Docker inspection showed only 127.0.0.1 mappings for lab ports. TCP connection attempts from Windows to 192.168.151.5:28088, :28089 and :28090 failed. No lab ports were exposed on a LAN/public interface.
- Opened the deployed tourism website in the browser through an authenticated SSH tunnel at http://127.0.0.1:38088 and captured `screenshots/horizon.png`.
- Host Apache remained active; checksums of `/etc/apache2/sites-enabled/zaatra.conf` and `/var/www/zaatra/public/index.php` remained unchanged across deployment.

## Limits

No exploit, memory-corruption chain, command-execution payload, reverse shell or exfiltration demonstration was executed. The patched service passed runtime, HTTP, configuration and exposure regression checks; this is not a penetration-test certification or a claim that every PHP vulnerability is fixed. Exploit/heap-layout reproducibility after UI customization was not revalidated. Automated functional checks do not replace full cross-browser, screen-reader or real-device testing.

Reservations remain fictional and client-side; there is no real booking backend or payment system. No accounts or invented university logos were added. The retained locked lab shell is upstream Windows-lab behavior and is not part of the tourism flow. `/out` state is ephemeral, with no shared host mounts.
