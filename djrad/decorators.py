import json
from functools import wraps

from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _

from djrad import types
from . import consts
from .exceptions import APIException


def _check_method(request, method):
    if request.method != method:
        raise APIException(
            message=_("invalid method, use {} instead").format(method),
            status=405
        )


def _get_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
    elif request.method == "GET":
        data = request.GET.copy()
    else:
        data = {}
    return data


def _check_required_params(data, required_params):
    for param in required_params:
        item = data.get(param)
        if not item:
            raise APIException(message=_("{} required").format(param), status=400, error_code=400)


def _check_params(params, required_params, param_types):
    for param in required_params:
        if not param in params:
            raise ValueError('required_params should be a subset of params')

    for key in param_types:
        if key not in params:
            raise ValueError('keys of param_types should be a subset of params')

    for key, value in param_types.items():
        if value not in types.ALLOWED_TYPES:
            raise ValueError("unknown type {}".format(value))


def _check_param_types(data, param_types):
    for key, value in param_types.items():
        item = data.get(key)
        if not item:
            continue
        if not types.validate(item, value):
            raise APIException(_("{} is not a valid {}").format(key, types.VERBOSE_TYPES[value]), status=400, error_code=400)


def api(method="GET", params=None, required_params=None, param_types=None, required_files=None):
    params = [] if not params else params
    required_params = [] if not required_params else required_params
    required_files = [] if not required_files else required_files
    param_types = {} if not param_types else param_types
    _check_params(params, required_params, param_types)

    def func(f):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            try:
                _check_method(request, method)

                data = _get_data(request)
                request.data = data

                _check_required_params(data, required_params)
                _check_required_params(request.FILES, required_files)
                _check_param_types(data, param_types)

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


def json_rpc():
    def func(f):
        @wraps(func)
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
