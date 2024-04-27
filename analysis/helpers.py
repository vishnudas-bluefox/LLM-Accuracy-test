import re


def extract_dicts_from_string(sample_string):
    dicts1 = re.findall(r'\{[^{}]*\}', sample_string)
    list_of_dicts1 = [eval(d) for d in dicts1]
    return list_of_dicts1