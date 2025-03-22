from functools import wraps

from django.http import HttpResponse

from .models import App


def api_key_required(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):

        if "Authorization" in request.headers:
            api_key = request.headers.get("Authorization").split(" ")[-1]
            try:
                app = App.objects.get(api_key=api_key)
                request._app = app

                return fn(request, *args, **kwargs)
            except App.DoesNotExist:
                pass
        return HttpResponse(status=403)

    return wrapper
