def sort_func(data):
    used = set()
    return [x for x in [item for item in data] if x not in used and (used.add(x) or True)]