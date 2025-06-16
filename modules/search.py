
def search_laws(laws_data, keyword):
    """Search for keyword in law clauses."""
    results = []
    for clause in laws_data.get("laws", []):
        if keyword in clause.get("조문내용", "") or keyword in clause.get("조문명", ""):
            results.append(clause)
    return results
