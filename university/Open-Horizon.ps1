# Interactive SSH authentication. No credentials are stored by this script.
$ErrorActionPreference = 'Stop'
Write-Host 'Keep this window open. Target: http://127.0.0.1:38088'
ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:38088:127.0.0.1:28088 -L 127.0.0.1:38089:127.0.0.1:28089 -L 127.0.0.1:38090:127.0.0.1:28090 root@192.168.151.5
