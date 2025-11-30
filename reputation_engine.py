"""Simple reputation engine to score aggregated intelligence."""
def score(results):
    # Very lightweight heuristic scoring: presence of breaches, blacklist entries, and social hits increase risk.
    score = 0
    details = {}
    # Email breaches
    if isinstance(results.get('results'), dict):
        # Called from main: handle full payload
        pass


class ReputationEngine:
    def score(self, payload):
        # payload contains 'results' and other metadata
        r = {'score': 0, 'factors': []}
        results = payload.get('results') if isinstance(payload, dict) else payload
        if not results:
            return r
        # check email breaches
        if isinstance(results, dict) and 'breaches' in results and results['breaches']:
            r['score'] += 40
            r['factors'].append('email_breach')
        # username social presence
        if isinstance(results, list):
            hits = sum(1 for x in results if x.get('exists'))
            if hits:
                r['score'] += min(30, hits * 5)
                r['factors'].append(f'social_hits_{hits}')
        # IP blacklists
        if isinstance(results, dict) and results.get('blacklist'):
            r['score'] += 20
            r['factors'].append('ip_blacklist')

        r['score'] = max(0, min(100, r['score']))
        return r
