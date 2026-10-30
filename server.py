import json, re, secrets, ipaddress, os
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
import dns.resolver, dns.exception
ROOT=Path(__file__).resolve().parent
entries=[]
for country,city,domain in re.findall(r'^"([^|\n"]+)\|([^|\n"]+)\|([^|\n"]+)"$',(ROOT/'Isp.txt').read_text(),re.M):
    entries.append({'country':country,'city':city,'domain':domain})
resolver=dns.resolver.Resolver(configure=True);resolver.timeout=2.5;resolver.lifetime=5

def lookup(domain,kind):
    try: return [str(x).rstrip('.') for x in resolver.resolve(domain,kind)]
    except (dns.exception.DNSException, OSError): return []

def generate(country,kind):
    pool=[e for e in entries if e['country']==country]
    if not pool: raise ValueError('Unknown country')
    item=secrets.choice(pool)
    ns=lookup(item['domain'],'NS')
    types=['A','AAAA'] if kind=='both' else [kind]
    addresses={t:[] for t in types}
    for name in ns[:16]:
        for t in types:
            for addr in lookup(name,t):
                try:
                    if ipaddress.ip_address(addr).version==(4 if t=='A' else 6) and addr not in addresses[t]:addresses[t].append(addr)
                except ValueError:pass
    return {**item,'nameservers':ns,'ipv4':addresses.get('A',[]),'ipv6':addresses.get('AAAA',[]),'note':'These are authoritative nameserver IPs, not verified public recursive DNS resolvers.'}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT/'static'),**kwargs)
    def json(self,data,status=200):
        raw=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def do_GET(self):
        if urlparse(self.path).path=='/api/countries':return self.json(sorted(set(e['country'] for e in entries)))
        return super().do_GET()
    def do_POST(self):
        if urlparse(self.path).path!='/api/generate':return self.json({'error':'Not found'},404)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length>2048 or length<=0:return self.json({'error':'Invalid payload'},400)
            data=json.loads(self.rfile.read(length));country=data.get('country');kind=data.get('type','both')
            if not isinstance(country,str) or kind not in ('A','AAAA','both'):return self.json({'error':'Invalid selection'},400)
            return self.json(generate(country,kind))
        except (ValueError, json.JSONDecodeError) as ex:return self.json({'error':str(ex)},400)
        except Exception:return self.json({'error':'DNS lookup failed'},502)
if __name__=='__main__':
    port=int(os.environ.get('PORT','8000'))
    print(f'R9 DNS Generator: http://localhost:{port}')
    ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
