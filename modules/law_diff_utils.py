from difflib import HtmlDiff

def compare_laws(old_html: str, new_html: str):
    """두 HTML 문자열을 비교하여 diff HTML로 반환한다."""
    differ = HtmlDiff()
    return differ.make_file(
        old_html.splitlines(),
        new_html.splitlines(),
        fromdesc="기존 법령",
        todesc="변경된 법령"
    )
