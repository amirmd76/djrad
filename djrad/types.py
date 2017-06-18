import json
import re

INTEGER = "int"
BOOLEAN = "bool"
STRING = "str"
EMAIL = "email"
ALPHA = "alpha"
ALPHANUMERIC = "alphanumeric"
STD = "std"
JSON = "json"
LIST = "list"
DICT = "dict"


def validate_integer(value):
    if not isinstance(value, int):
        raise ValueError('Not an integer')


def validate_boolean(value):
    if not isinstance(value, bool):
        raise ValueError('Not a boolean')


def validate_string(value):
    if not isinstance(value, str):
        raise ValueError('Not an string')


def validate_email(value):
    value = validate_string(value)
    if not bool(re.match(r"[^@]+@[^@]+\.[^@]+", value)):
        raise ValueError('Not an email')
    return value


def validate_alpha(value):
    value = validate_string(value)

    if not bool(re.match(r"^[a-zA-Z]+$", value)):
        raise ValueError("Not an alphabetic string")
    return value


def validate_alphanumeric(value):
    value = validate_string(value)

    if not bool(re.match(r"^[a-zA-Z0-9]+$", value)):
        raise ValueError("Not an alphanumeric string")


def validate_standard_string(value):
    value = validate_string(value)

    if not bool(re.match(r"^[a-zA-Z0-9_]+$", value)):
        raise ValueError("Not an standard string")


def validate_json(value):
    try:
        json.loads(value)
    except:
        raise ValueError("Not a JSON")


def validate_list(value):
    if not isinstance(value, list):
        raise ValueError('Not an list')


def validate_dict(value):
    if not isinstance(value, dict):
        raise ValueError('not a dictionary')

ALLOWED_TYPES = {INTEGER: validate_integer,  BOOLEAN: validate_boolean, STRING: validate_string, EMAIL: validate_email, ALPHA: validate_alpha,
                 ALPHANUMERIC: validate_alphanumeric, STD: validate_standard_string, JSON: validate_json, LIST: validate_list, DICT: validate_dict}


VERBOSE_TYPES = {INTEGER: "integer", BOOLEAN: "boolean", STRING: "string", EMAIL: "email", ALPHA: "alphabetic string",
                 ALPHANUMERIC: "alphanumeric string", STD: "standard string", JSON: "JSON", LIST: "list", DICT: "dictionary"}


def validate(value, type):
    try:
        ALLOWED_TYPES[type](value)
        return True
    except:
        return False
