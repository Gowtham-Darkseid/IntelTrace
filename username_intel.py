"""Username reconnaissance across major platforms (public profile existence checks)."""
import requests
from concurrent.futures import ThreadPoolExecutor

PLATFORMS = {
    'github': 'https://github.com/{}',
    'x': 'https://x.com/{}',
    'twitter': 'https://twitter.com/{}',
    'reddit': 'https://www.reddit.com/user/{}',
    'instagram': 'https://www.instagram.com/{}',
    'facebook': 'https://www.facebook.com/{}',
    'medium': 'https://medium.com/@{}'
}


class UsernameIntel:
    def __init__(self, timeout=8):
        self.s = requests.Session()
        self.timeout = timeout

    def check_profile(self, platform, username):
        url = PLATFORMS.get(platform).format(username)
        try:
            r = self.s.head(url, allow_redirects=True, timeout=self.timeout)
            return {'platform': platform, 'exists': r.status_code in (200, 301, 302), 'url': r.url, 'status_code': r.status_code}
        except Exception:
            return {'platform': platform, 'exists': False, 'url': url, 'status_code': None}

    def darkweb_sim(self, username):
        # Tor-based checks would be performed here. This is a simulation placeholder.
        return {'tor_presence_simulation': False}

    def collect(self, username):
        results = []
        with ThreadPoolExecutor(max_workers=6) as ex:
            futures = [ex.submit(self.check_profile, p, username) for p in PLATFORMS.keys()]
            for f in futures:
                results.append(f.result())
        results.append(self.darkweb_sim(username))
        return results
