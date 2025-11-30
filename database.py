import os
import json
import glob


class IntelDB:
    def __init__(self):
        self.reports_dir = 'reports'
        os.makedirs(self.reports_dir, exist_ok=True)
        print('[db] Using JSON file storage')

    def save_case(self, case):
        case_id = case['case_id']
        json_path = os.path.join(self.reports_dir, f"{case_id}.json")
        with open(json_path, 'w') as f:
            json.dump(case, f, indent=2)
        print('[db] Saved to JSON file')

    def get_case(self, case_id):
        json_path = os.path.join(self.reports_dir, f"{case_id}.json")
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                return json.load(f)
        return None

    def list_cases(self):
        """List all cases from JSON files."""
        cases = []
        json_files = glob.glob(os.path.join(self.reports_dir, '*.json'))
        for json_path in json_files:
            with open(json_path, 'r') as f:
                cases.append(json.load(f))
        
        return sorted(cases, key=lambda x: x.get('case_id', ''), reverse=True)
