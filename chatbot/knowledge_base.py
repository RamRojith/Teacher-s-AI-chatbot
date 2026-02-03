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
            return {}
        with open(DOCS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)

    def search_help(self, query):
        """
        Simple keyword matching. Returns the response if keywords match.
        """
        query_lower = query.lower()
        if not self.data: return None
        
        for key, content in self.data.items():
            if any(k in query_lower for k in content.get('keywords', [])):
                return content.get('response')
        return None

    def get_help_text(self, role):
        if role == 'HOD':
            return "As HOD, you can:\n- List students of your department or assigned sections.\n- Analyze performance of your department students.\n- View subject-specific class reports."
        elif role == 'Vice Principal':
            return "As VP, you have institutional access to all student profiles, marks, and reports."
        elif role in ['Advisor', 'CA', 'Teacher', 'Faculty']:
            return "You can:\n- List students in your assigned subjects and sections.\n- Analyze performance of your specific students.\n- Submit class reports to the advisor."
        return "I can help you analyze student performance and navigate ERP data. Please specify your request."
