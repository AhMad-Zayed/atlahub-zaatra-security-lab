# Horizon deployment and rollback

Destination: authorized Ubuntu `horizon-test`, accessed using SSH. Credentials are never included in source, commands or image archives. Installation directory: `/opt/atlahub-zaatra-university`. Existing `/var/www/zaatra` and host Apache port 80 are independent.

Docker Engine and Compose were absent initially. They were installed from Docker's official signed Ubuntu noble apt repository following https://docs.docker.com/engine/install/ubuntu/ . Nmap was installed from Ubuntu apt for the requested header discovery. No host Apache configuration was changed. Packages remain installed after lab shutdown, to avoid affecting later workloads.

## Exact-image deployment

Build and validate all three images on the source machine first. Export the images together, transfer using SFTP/SCP, verify archive SHA-256, and load the archive. Do not rebuild on Horizon when exact-image parity is required. `IMAGE-MANIFEST.json` records image IDs and the gzip archive checksum. The transferred archive is retained beside the configuration on Horizon.

```sh
docker save -o zaatra-images.tar atlahub/zaatra-university:vulnerable-8.4.26 atlahub/zaatra-university:mitigated-8.4.26 atlahub/zaatra-university:patched-8.4.27
# Compress, checksum and transfer with your approved SSH tooling.
# On Horizon:
cd /opt/atlahub-zaatra-university
docker load -i zaatra-images.tar.gz
docker compose up -d --no-build --pull never
docker compose ps
python3 validate.py
```

Inspect the host before deploying: architecture, free disk, Docker/Compose version, `ss -lnt`, existing containers and Apache state. Do not overwrite a preexisting deployment directory. The source Dockerfile uses pinned upstream base digests for future rebuilds. A future rebuild is a new artifact and requires fresh validation.

## Authenticated SSH access

From Windows PowerShell, keep this command running (authenticate interactively with your existing SSH credentials):

```powershell
ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:38088:127.0.0.1:28088 -L 127.0.0.1:38089:127.0.0.1:28089 -L 127.0.0.1:38090:127.0.0.1:28090 root@192.168.151.5
```

Then open http://127.0.0.1:38088 (target), http://127.0.0.1:38089 (patched), or http://127.0.0.1:38090 (mitigated). Remote ports 28088–28090 are loopback-only. Ctrl+C closes the tunnel. Do not browse the vulnerable service through a public or LAN port mapping.

Observed SSH host key SHA-256 at first connection: `tCIWNgx7TIUh81Q9KZqePCMOFkq9jB96eeKIYmwpYjM=`. Subsequent deployment tooling pinned this key; independently compare it to server console/administrator records before establishing trust on another machine. No private SSH key or new authorized_keys entry was installed.

## Rollback and cleanup

This installation is additive. To stop the lab and remove its containers and project network:

```sh
cd /opt/atlahub-zaatra-university
docker compose down
```

This discards ephemeral `/out` state. The preexisting Zaatra application and Apache continue operating. Retain the source and image archive for restart with `docker compose up -d --no-build --pull never`. For an upgrade, keep the prior image IDs and a versioned config directory, deploy only after validation, and roll back by loading the previous archive with its original Compose file.

Full cleanup is optional and must be performed only after explicit approval: stop this Compose project, confirm no other containers use the three `atlahub/zaatra-university` tags, remove only those tags, and remove only the verified `/opt/atlahub-zaatra-university` directory. Do not run broad image/system prune, remove Docker packages, or alter `/var/www/zaatra` or `/etc/apache2`. No destructive cleanup has been performed.
