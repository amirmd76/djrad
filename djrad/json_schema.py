from jsonschema import Draft4Validator, ErrorTree

from djrad.consts import PROPERTIES, MISSED_KEYS
from djrad.types import ALLOWED_TYPES, FILE


def get_schema(required_params, param_types):
    schema = {"type": "object", "required": required_params}
    properties = {}
    for key, value in param_types.items():
        if value in ALLOWED_TYPES:
            properties[key] = ALLOWED_TYPES[value]
        else:
            properties[key] = value
    schema['properties'] = properties
    return schema


def validate(schema, value):
    validator = Draft4Validator(schema)
    if validator.is_valid(value):
        return {}

    tree = ErrorTree(validator.iter_errors(value))

    result_errors = {}

    for key, value in tree.errors.items():
        result_errors[key] = value.message

    for key in tree:
        print(key, tree[key].errors)
        errors = {}
        for error in tree[key].errors:
            errors[error] = tree[key].errors[error].message
        if errors:
            result_errors[key] = errors

    return result_errors


def validate_params(required_params, param_types, data):
    schema = get_schema(required_params, param_types)
    return validate(schema, data)


def validate_schema(schema):
    meta = Draft4Validator.META_SCHEMA.copy()
    meta[PROPERTIES].update(MISSED_KEYS)
    if not Draft4Validator(meta).is_valid(schema):
        raise ValueError("{} is not a valid json schema".format(schema))
