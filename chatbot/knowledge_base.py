import json
import os

# Get path relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_PATH = os.path.join(BASE_DIR, "..", "data", "erp_docs.json")

class KnowledgeBase:
    def __init__(self):
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(DOCS_PATH):
            print(f"DEBUG: KnowledgeBase could not find docs at {DOCS_PATH}")
            return {}
        with open(DOCS_PATH, 'r') as f:
            return json.load(f)

    def search_help(self, query):
        """
        Simple keyword matching. Returns the response if keywords match.
        """
        query_lower = query.lower()
        best_match = None
        max_matches = 0

        for key, content in self.data.items():
            matches = sum(1 for k in content['keywords'] if k in query_lower)
            if matches > max_matches:
                max_matches = matches
                best_match = content['response']
        
        if max_matches > 0:
            return best_match
        return None
