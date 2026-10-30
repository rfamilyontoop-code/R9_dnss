# R9 DNS Generator

A bilingual (English/Persian) web application using the country/city/ISP domain entries from Isp.txt. On each click, one entry from the selected country is selected using a cryptographic random choice, then the backend queries NS records for that domain and A/AAAA records of its nameservers.

## Run

Requires Python 3.9+ and internet access for live DNS queries.

```bash
python -m pip install -r requirements.txt
python server.py
```

Open http://localhost:8000 . To deploy publicly, run behind HTTPS reverse proxy and use a managed process with rate limiting. PORT environment variable is supported.

**Important:** This reproduces the original script's DNS lookup logic, not an assurance that returned IPs are publicly usable recursive DNS resolvers. DNS records may be absent or queries may time out. The backend only accepts countries from the bundled allowlist.
