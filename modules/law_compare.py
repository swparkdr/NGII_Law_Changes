import difflib

def compare_laws(old_html: str, new_html: str):
    old_lines = old_html.splitlines()
    new_lines = new_html.splitlines()

    diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=""))
    added = [line[1:] for line in diff if line.startswith("+") and not line.startswith("+++")]
    removed = [line[1:] for line in diff if line.startswith("-") and not line.startswith("---")]

    summary = f"{len(removed)}줄 삭제됨, {len(added)}줄 추가됨"
    return added, removed, summary
