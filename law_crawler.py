import json

def load_law_changes(filepath='data/law_changes.json'):
    """Load mock law change data from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
