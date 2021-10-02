def _replace_hyphen_with_underscore(d:dict) -> dict:
    d_keys = list(d.keys())
    for key in d_keys:
        new_key = key.replace("-", "_")
        d[new_key] = d.pop(key)
    return d
