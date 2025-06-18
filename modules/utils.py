from difflib import ndiff

def highlight_differences(old_text, new_text):
    """Highlight differences between two texts."""
    diff = ndiff(old_text.split(), new_text.split())
    return " ".join(diff)