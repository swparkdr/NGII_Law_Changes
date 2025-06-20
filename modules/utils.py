from difflib import SequenceMatcher

def highlight_differences(old_text, new_text):
    s = SequenceMatcher(None, old_text.splitlines(), new_text.splitlines())
    result = []

    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            result.extend([f"<div>{line}</div>" for line in old_text.splitlines()[i1:i2]])
        elif tag == 'replace':
            result.extend([f"<div style='color:red'>- {line}</div>" for line in old_text.splitlines()[i1:i2]])
            result.extend([f"<div style='color:green'>+ {line}</div>" for line in new_text.splitlines()[j1:j2]])
        elif tag == 'delete':
            result.extend([f"<div style='color:red'>- {line}</div>" for line in old_text.splitlines()[i1:i2]])
        elif tag == 'insert':
            result.extend([f"<div style='color:green'>+ {line}</div>" for line in new_text.splitlines()[j1:j2]])

    return "\n".join(result)
