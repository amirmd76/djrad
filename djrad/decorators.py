import json
from functools import wraps

from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from djrad import types
from djrad.json_schema import validate_schema, validate_params
from djrad import consts
from djrad.exceptions import APIException
from djrad.types import FILE


def _check_method(request, method):
    if request.method != method:
        raise APIException(
            message=_("invalid method, use {} instead").format(method),
            status=405
        )


def _get_data(request):
    data = {}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except ValueError:
            pass
    elif request.method == "GET":
        data = request.GET.copy()
    return data


def _check_required_files(data, required_files):
    errors = {}
    for param in required_files:
        item = data.get(param)
        if not item:
            errors[param] = 'required'

    return errors


def _check_params(params, required_params, param_types):
    for param in required_params:
        if param not in params:
            raise ValueError('required_params should be a subset of params')

    for key in param_types:
        if key not in params:
            raise ValueError('keys of param_types should be a subset of params')

    for key, value in param_types.items():
        if value not in types.ALLOWED_TYPES:
            validate_schema(value)


def _extract_required_and_type(param):
    if len(param) > 3:
        raise ValueError("Param len should be at most 3")
    if len(param) == 1:
        return False, None
    if len(param) == 2:
        if isinstance(param[1], bool):
            return param[1], None
        else:
            return False, param[1]
    is_bool = [False, False]
    for i in range(1, 3):
        if isinstance(param[i], bool):
            is_bool[i-1] = True
    if not (is_bool[0] ^ is_bool[1]):
        raise ValueError("Exactly one of param[1] and param[2] should be boolean (required)")
    for i in range(1, 3):
        if is_bool[i-1]:
            return param[i], param[3-i]


def _extract_params(raw_params):
    params = []
    required_params = []
    param_types = {}
    required_files = []
    files = []

    if raw_params:
        for raw_param in raw_params:
            if not isinstance(raw_param, tuple):
                params.append(raw_param)
            else:
                if len(raw_param) < 1:
                    raise ValueError("param can not be empty")
                else:
                    param_name = raw_param[0]
                    required, expected_type = _extract_required_and_type(raw_param)
                    if expected_type == FILE:
                        files.append(param_name)
                        if required:
                            required_files.append(param_name)
                        continue
                    params.append(param_name)
                    if required:
                        required_params.append(param_name)
                    if expected_type:
                        param_types[param_name] = expected_type

    return params, files, required_params, param_types, required_files


def _check_data(required_params, param_types, required_files, data, files):
    errors = {}
    errors.update(_check_required_files(files, required_files))
    dict_data = dict(data)
    errors.update(validate_params(required_params, param_types, dict_data))

    return errors


def api(method="GET", params=None, required_params=None, param_types=None, required_files=None):
    params = [] if not params else params
    required_params = [] if not required_params else required_params
    required_files = [] if not required_files else required_files
    param_types = {} if not param_types else param_types
    _check_params(params, required_params, param_types)

    def func(f):
        @wraps(func)
        @csrf_exempt
        def wrapped(request, *args, **kwargs):
            try:
                _check_method(request, method)

                data = _get_data(request)
                request.data = data

                errors = _check_data(required_params, param_types, required_files, data, request.FILES)
                if errors:
                    return JsonResponse({
                        consts.RESULT: consts.ERROR,
                        consts.ERROR: errors
                    }, status=400)

                result_params = {}
                for param in params:
                    result_params[param] = data.get(param, None)

                new_kwargs = kwargs.copy()
                new_kwargs.update(result_params)

                r = f(request, *args, **new_kwargs) or {}

                result = {consts.RESULT: consts.SUCCESS}
                result.update(r)
                return JsonResponse(result)

            except APIException as api_exception:
                return JsonResponse({
                    consts.RESULT: consts.ERROR,
                    consts.ERROR: {
                        consts.CODE: api_exception.error_code,
                        consts.MESSAGE: api_exception.message,
                    }
                }, status=api_exception.status)

        return wrapped

    return func


def rest_api(method="GET", params=None):
    raw_params = params

    params, files, required_params, param_types, required_files = _extract_params(raw_params)
    _check_params(params, required_params, param_types)

    def func(f):
        @wraps(func)
        @csrf_exempt
        def wrapped(request, *args, **kwargs):
            try:
                _check_method(request, method)

                data = _get_data(request)
                request.data = data

                errors = _check_data(required_params, param_types, required_files, data, request.FILES)
                if errors:
                    return JsonResponse({
                        consts.RESULT: consts.ERROR,
                        consts.ERROR: errors
                    }, status=400)

                result_params = {}
                for param in params:
                    result_params[param] = data.get(param, None)

                for param in files:
                    result_params[param] = request.FILES.get(param, None)

                new_kwargs = kwargs.copy()
                new_kwargs.update(result_params)

                r = f(request, *args, **new_kwargs) or {}

                result = {consts.RESULT: consts.SUCCESS}
                result.update(r)
                return JsonResponse(result)

            except APIException as api_exception:
                return JsonResponse({
                    consts.RESULT: consts.ERROR,
                    consts.ERROR: {
                        consts.CODE: api_exception.error_code,
                        consts.MESSAGE: api_exception.message,
                    }
                }, status=api_exception.status)

        return wrapped

    return func


def json_rpc():
    def func(f):
        @wraps(func)
        @csrf_exempt
        def wrapped(request, *args, **kwargs):
            try:
                r = f(request, *args, **kwargs) or {}

                result = {consts.ERROR: 0}
                result.update(r)
                return result

            except APIException as api_exception:
                return {
                    consts.ERROR: api_exception.error_code
                }

        return wrapped

    return func
