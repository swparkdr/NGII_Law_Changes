def load_json_file(filepath):
    """Load JSON data from a file path."""
    import json
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def highlight_differences(old_text, new_text):
    """Highlight differences between two texts."""
    from difflib import ndiff
    diff = ndiff(old_text.split(), new_text.split())
    return " ".join(diff)
