"""IP intelligence: WHOIS, geolocation, ASN, ISP, VPN/proxy checks."""
import os
import requests
import whois
from dotenv import load_dotenv

load_dotenv()
TOR_PROXY = os.getenv('TOR_PROXY')


class IPIntel:
    def __init__(self, use_tor=False):
        self.session = requests.Session()
        if use_tor and TOR_PROXY:
            self.session.proxies.update({'http': TOR_PROXY, 'https': TOR_PROXY})

    def whois_lookup(self, ip):
        try:
            return whois.whois(ip)
        except Exception:
            return {}

    def ipinfo_lookup(self, ip):
        # Uses ipinfo.io free endpoint (no key). For production use, add keys.
        try:
            r = self.session.get(f'https://ipinfo.io/{ip}/json', timeout=10)
            return r.json()
        except Exception:
            return {}

    def blacklist_check(self, ip):
        # Simple heuristic; call public blacklists if configured.
        # Placeholder returns empty list
        return []

    def detect_vpn_proxy(self, ip):
        # Placeholder: rely on external services for production.
        return {'vpn': False, 'proxy': False}

    def collect(self, ip):
        data = {}
        data['whois'] = self.whois_lookup(ip)
        data['ipinfo'] = self.ipinfo_lookup(ip)
        data['blacklist'] = self.blacklist_check(ip)
        data['vpn_proxy'] = self.detect_vpn_proxy(ip)
        return data
