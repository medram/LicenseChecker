from functools import wraps

from django.http import HttpResponse

from .models import App


def api_key_required(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        print("in wrapper")

        if "Authorization" in request.headers:
            api_key = request.headers.get("Authorization").split(" ")[-1]
            print(f"api_key: {api_key}")
            try:
                app = App.objects.get(api_key=api_key)
                print(f"app: {app}")
                request._app = app

                return fn(request, *args, **kwargs)
            except App.DoesNotExist:
                pass
        return HttpResponse(status=403)

    return wrapper
