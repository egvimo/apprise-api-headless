def parse_tag_expression(expr: str | None):
    """
    Convert a tag expression string into the structured format Apprise expects.

    Rules:
      - Top-level comma-separated entries = OR
      - Space-separated entries within each part = AND
      - Single tag = string
      - Multiple tags = tuple

    Examples:
      "tagA"               -> ['tagA']
      "tagA, tagB"         -> ['tagA', 'tagB']
      "tagA tagC, tagB"    -> [('tagA','tagC'), 'tagB']
      "tagB tagC"          -> [('tagB','tagC')]
    """
    if not expr:
        return None

    expr = expr.strip()

    groups = []
    for part in expr.split(","):
        tags = [t for t in part.strip().split() if t]
        if not tags:
            continue
        groups.append(tags[0] if len(tags) == 1 else tuple(tags))
    return groups
