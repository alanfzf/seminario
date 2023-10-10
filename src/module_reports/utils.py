import re

__BASE_NAME__ = "a-zA-ZÁ-Úá-ú"


PATTERN_NAMES = re.compile(
    "^([{name}]+( [{name}]+)*)(, ?([{name}]+( [{name}]+)*))*$"
    .format(name=__BASE_NAME__)
)

PATTERN_NAMES_AND_AGES = re.compile(
    "^([{name}]+( [{name}]+)*: \d+)(, ?([{name}]+( [{name}]+)*: \d+))*$"
    .format(name=__BASE_NAME__)
)

def valid_names(data):
    return re.match(PATTERN_NAMES, data)

def valid_names_and_ages(data):
    return re.match(PATTERN_NAMES_AND_AGES, data)
