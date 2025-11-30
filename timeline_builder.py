"""Simple timeline builder that extracts timestamps and orders events."""
from datetime import datetime


class TimelineBuilder:
    def build(self, results):
        # Very simple: create timestamped entries for discovered items
        events = []
        t0 = datetime.utcnow().isoformat() + 'Z'
        events.append({'time': t0, 'desc': 'Collection started'})
        if isinstance(results, dict):
            for k, v in results.items():
                events.append({'time': t0, 'desc': f'Collected {k}'})
        elif isinstance(results, list):
            events.append({'time': t0, 'desc': f'Found {len(results)} items'})
        events.append({'time': datetime.utcnow().isoformat() + 'Z', 'desc': 'Analysis complete'})
        return events
