import pandas as pd

def load_internal_docs(filepath='data/internal_docs.csv'):
    """Load internal document metadata from CSV."""
    return pd.read_csv(filepath)

def match_law_to_docs(law_change, internal_docs):
    """Match law change to internal document items using keywords."""
    matches = []

    # Prepare text for keyword matching
    text = f"{law_change['제목']} {law_change['변경사항']}"

    for _, row in internal_docs.iterrows():
        keywords = row['관련키워드'].split(';')
        for kw in keywords:
            if kw.strip() in text:
                matches.append({
                    "문서명": row['문서명'],
                    "항목명": row['항목명'],
                    "매칭키워드": kw.strip()
                })
                break

    return matches
