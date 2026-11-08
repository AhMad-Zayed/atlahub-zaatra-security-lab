"""Non-destructive acceptance checks. Python 3 standard library only."""
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from pathlib import Path
import subprocess,json,hashlib,sys

ROOT=Path(__file__).resolve().parent
def docker(*args):
 return subprocess.check_output(['docker','compose','-f',str(ROOT/'compose.yaml'),*args],text=True).strip()
def request(port,path='/',method='GET'):
 try:
  with urlopen(Request(f'http://127.0.0.1:{port}{path}',method=method),timeout=15) as r:return r.status,dict(r.headers),r.read()
 except HTTPError as r:return r.code,dict(r.headers),r.read()
def check(ok,description):
 if not ok:raise AssertionError(description)
 print('PASS:',description)
for service,port,version in [('vulnerable',28088,'8.4.26'),('mitigated',28090,'8.4.26'),('patched',28089,'8.4.27')]:
 for method in ['HEAD','GET']:
  code,headers,body=request(port,method=method)
  check(code==200 and headers.get('X-Powered-By')=='PHP/'+version,f'{service}: {method}, actual PHP header {version}')
  if method=='GET':
   text=body.decode();check('Developed and Customized by AtlaHub Tech' in text and 'Prepared Exclusively for Palestine Ahliya University' in text and 'Zaatra Tourism &amp;' not in text and 'Zaatra Tourism & Travel' in text,f'{service}: branding and attribution')
   check('Content-Security-Policy' in headers and headers.get('X-Frame-Options')=='DENY',f'{service}: browser protection headers')
 status=json.loads(request(port,'/status.php')[2]);check(status['php_version']==version and status['sapi']=='apache2handler' and status['variant']==service,f'{service}: mod_php and variant')
 check((status['session_upload_progress_enabled'] in ('','0')) if service=='mitigated' else status['session_upload_progress_enabled']=='1',f'{service}: preserved upload-progress setting')
 cid=docker('ps','-q',service)
 inspect=json.loads(subprocess.check_output(['docker','inspect',cid],text=True))[0]
 check(inspect['State']['Health']['Status']=='healthy',f'{service}: healthy without HTTP health probes')
 bindings=inspect['NetworkSettings']['Ports']['80/tcp'];check(all(b['HostIp']=='127.0.0.1' for b in bindings),f'{service}: loopback-only binding')
 digest=docker('exec','-T',service,'sha256sum','/opt/atlahub-training/training-evidence.jpg').split()[0]
 check(digest==(ROOT/'evidence/SHA256SUMS').read_text().split()[0],f'{service}: training image checksum')
 for path in ['/training-evidence.jpg','/opt/atlahub-training/training-evidence.jpg']:
  check(request(port,path)[0]==404,f'{service}: evidence outside document root {path}')
 check(request(port,'/shell.php','POST')[0]==403,f'{service}: existing lab shell remains locked')
 for asset in ['jerusalem.jpg','petra.jpg','istanbul.jpg','zaatra.css','zaatra.js']:
  check(request(port,'/assets/'+asset)[0]==200,f'{service}: bundled asset {asset}')
 for file in ['index.php','status.php','probe.php','shell.php']:
  docker('exec','-T',service,'php','-l','/var/www/html/'+file)
 check(True,f'{service}: PHP syntax checks')
print('All non-destructive acceptance checks passed. No exploit or reverse shell was executed.')
