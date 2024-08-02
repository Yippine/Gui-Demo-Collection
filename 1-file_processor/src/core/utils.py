import re

def convert_to_regex(patterns):
    return [re.compile(pattern.replace("*", ".*").replace("?", ".")) for pattern in patterns]
