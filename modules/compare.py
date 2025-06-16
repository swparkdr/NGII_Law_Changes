import json

def compare_laws(old_path, new_path):
    """
    Compare two versions of law JSON files.

    Parameters:
    - old_path: file path to old laws JSON
    - new_path: file path to new laws JSON

    Returns:
    - A list of differences between old and new laws
    """
    with open(old_path, encoding="utf-8") as f:
        old_laws = {item["조문명"]: item["조문내용"] for item in json.load(f).get("laws", [])}
    with open(new_path, encoding="utf-8") as f:
        new_laws = {item["조문명"]: item["조문내용"] for item in json.load(f).get("laws", [])}

    diff = []
    for name, new_content in new_laws.items():
        old_content = old_laws.get(name)
        if old_content and old_content.strip() != new_content.strip():
            diff.append({
                "조문명": name,
                "이전": old_content,
                "현재": new_content
            })
    return diff
