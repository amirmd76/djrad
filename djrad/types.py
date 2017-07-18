INTEGER = "int"
FLOAT = "float"
BOOLEAN = "bool"
STRING = "str"
EMAIL = "email"
ALPHA = "alpha"
ALPHANUMERIC = "alphanumeric"
STD = "std"
LIST = "list"
DICT = "dict"
FILE = "file"

ALLOWED_TYPES = {INTEGER: {"type": "integer"}, FLOAT: {"type": "number"}, BOOLEAN: {"type": "boolean"}, STRING: {"type": "string"},
                 EMAIL: {"type": "string", "format": "email"}, ALPHA: {"type": "string", "pattern": r"^[a-zA-Z]+$"},
                 ALPHANUMERIC: {"type": "string", "pattern": r"^[a-zA-Z0-9]+$"}, STD: {"type": "string", "pattern": r"^[a-zA-Z0-9_]+$"},
                 LIST: {"type": "array"}, DICT: {"type": "object"}}
