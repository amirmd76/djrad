from functools import wraps

from django.http import JsonResponse

from . import consts
from .exceptions import APIException


def _check_method(request, method):
    if request.method != method:
        raise APIException(
            message="invalid method, use {} instead".format(method),
            status=405
        )


def api(method="GET"):
    def func(f):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            try:
                _check_method(request, method)

                r = f(request, *args, **kwargs) or {}

                result = {consts.RESULT: consts.SUCCESS}
                result.update(r)
                return JsonResponse(result)

            except APIException as api_exception:
                return JsonResponse({
                    consts.RESULT: consts.ERROR,
                    consts.MESSAGE: api_exception.message,
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
