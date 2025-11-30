"""Email intelligence: breach checks and domain reputation."""
import requests
import os
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()


class EmailIntel:
    def __init__(self, use_tor=False):
        self.session = requests.Session()

    def breach_check(self, email):
        # Uses haveibeenpwned API pattern but without API key here.
        # This is a placeholder; production should use HIBP API with key.
        try:
            url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}'
            r = self.session.get(url, timeout=10, headers={'User-Agent': 'IntelTrace'})
            if r.status_code == 200:
                return r.json()
            return []
        except Exception:
            return []

    def domain_reputation(self, domain):
        # Basic WHOIS + DNS reputation placeholder
        return {'domain': domain, 'reputation': 'unknown'}

    def collect(self, email):
        data = {}
        domain = email.split('@')[-1]
        data['breaches'] = self.breach_check(email)
        data['domain_reputation'] = self.domain_reputation(domain)
        return data
