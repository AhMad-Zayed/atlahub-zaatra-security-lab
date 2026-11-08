# Zaatra Tourism & Travel — University Edition

Developed and Customized by AtlaHub Tech  
Prepared Exclusively for Palestine Ahliya University  
Developer: Ahmad Jamil Othman – Zayed  
Faculty of Engineering & Information Technology — Cybersecurity Track

Arabic-first fictional travel agency for an authorized private university lab. Destination filters, a mobile navigation menu, trip selection and a client-side reservation summary work without accounts, payments or customer storage. All prices and itineraries are fictional. No official university logo is used.

## Attribution and provenance

This branch retains the complete upstream Git history, MIT LICENSE, NOTICE and third-party licenses of [RedSideSecurity/php2shell](https://github.com/RedSideSecurity/php2shell). Credit for the original research and low-level primitives belongs to the original contributors, including RedSide Security and 3em0 as described by NOTICE. AtlaHub Tech developed the tourism UI and university packaging; it does not claim invention of the original research. Institutional exclusivity refers to the university customization, and does not restrict rights under the original open-source licenses.

The existing Windows lab was a separate checkout with different history (`f301b1c3da58a0385e981f5856984fa55fadd913`). Its PHP settings, Apache single-worker configuration, status/probe and locked shell files were copied byte-for-byte into `university/`. Existing research source, payloads, offsets and primitives in both checkouts were not changed or run. `compose.windows.original.yaml` is a reference snapshot, not the deployment entry point.

## Start locally

Requires Linux containers / Docker Compose v2 or newer, amd64. Run from this directory:

```sh
docker compose build
docker compose up -d --no-build
docker compose ps
python3 validate.py
```

| Service | Actual PHP | Loopback URL |
|---|---|---|
| vulnerable | 8.4.26 | http://127.0.0.1:28088 |
| mitigated | 8.4.26 | http://127.0.0.1:28090 |
| patched | 8.4.27 | http://127.0.0.1:28089 |

Images use the original official PHP/Apache digests, Apache/mod_php, single prefork worker, KeepAlive Off and the exact original variant INI files. No extra PHP extensions or OS packages are installed in the application images. The separate Compose project leaves original Windows ports 18088, 8090 and 18089 untouched. Images contain their own website and configuration; there are no Windows bind mounts or shared runtime data. `/out` is container-local, writable by www-data and ephemeral; removal discards lab artifacts. No activation token is packaged.

Health checks inspect PID 1 and TCP listening state without sending HTTP requests. Active PHP probes during a research session could affect worker state; run acceptance checks outside such sessions. Logs rotate at 5 MB, two files per service:

```sh
docker compose logs --tail 50
docker compose exec -T patched php -v
```

The bridge has masquerading disabled, preserving the original lab setting. All published ports explicitly bind 127.0.0.1. This is not a comprehensive sandbox against a malicious host, other host administrators, or other containers on the same bridge. Do not add public port mappings, a public reverse proxy, or attach untrusted workloads. `internal: true` was tested locally but removed because this Docker Desktop release suppresses published ports on internal networks; it is not part of the final configuration.

## Assets and fictional training evidence

All website imagery is bundled locally with sources, author and license recorded in `ASSET-CREDITS.json` and the visible `/credits.html` page. The Wikimedia photographs retain their CC BY-SA terms, including attribution and share-alike requirements applicable to adaptations. CSS crops their display. Original UI code and fictional content were authored for this edition. There are no remote fonts, scripts or image dependencies.

The harmless image is **`/opt/atlahub-training/training-evidence.jpg`**, outside Apache's document root. It contains fictional labels only. SHA-256:

```text
1c1299b135aa204196cd394d1548968128943110b1bd1a6e64cfbf438d80552e
```

Verify using authorized container inspection:

```sh
docker compose exec -T vulnerable sh -c 'cd /opt/atlahub-training && sha256sum -c SHA256SUMS'
```

Ordinary photos are public local `/assets/*.jpg` resources. The training evidence has no HTTP retrieval route. No exfiltration feature was added. The Windows lab's existing token-locked `shell.php` was preserved unchanged, and remains locked without a token; the UI does not link to it. Do not use this lab as a general production site.

## Deliberate PHP header disclosure

The original INI setting `expose_php=On` produces the actual runtime `X-Powered-By` header. There is no hardcoded version header in the website or Apache configuration.

```sh
curl -I http://127.0.0.1:28088/
curl -sD - -o /dev/null http://127.0.0.1:28088/
nmap -sT -Pn -p 28088,28089,28090 --script http-headers --script-args 'http-headers.path=/' 127.0.0.1
```

Disclosure is deliberate and limited to the private educational deployment. PHP 8.4.27 is the requested comparison image, not a claim that it addresses every present or future PHP issue. For a hardened non-lab deployment, use a currently supported patched PHP image, `expose_php=Off`, `display_errors=Off`, an appropriate multiworker configuration, HTTPS and normal production access controls. Those production changes are intentionally outside this reproducible lab.

See [DEPLOYMENT.md](DEPLOYMENT.md), [TEST-RESULTS.md](TEST-RESULTS.md) and [screenshots](screenshots/) for operation and evidence.
