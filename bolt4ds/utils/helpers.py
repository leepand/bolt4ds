import re


_canonicalize_regex = re.compile("[-_]+")

def canonicalize_name(name):  # type: (str) -> str
    return _canonicalize_regex.sub("-", name).lower()


def module_name(name):  # type: (str) -> str
    """module_name("le-df")
       >>>'le_df'
    """
    return canonicalize_name(name).replace(".", "_").replace("-", "_")

def merge_dicts(d1, d2):
    """d1={"x":10} d2={"z":10,"k":102}
       print(d1)
       >>> {'x': 10, 'z': 10, 'k': 102}
    """
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], Mapping):
            merge_dicts(d1[k], d2[k])
        else:
            d1[k] = d2[k]
            