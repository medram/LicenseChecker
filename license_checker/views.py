import os
from typing import Any

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .decorators import api_key_required
from .models import App, Domain, License

ENVATO_TOKEN = os.getenv("ENVATO_TOKEN", None)


@csrf_exempt
@api_key_required
def check_license(request):

    result: dict[str, Any] = {}

    if request.method == "POST":
        license_code = request.POST.get("license_code")
        host = request.POST.get("host")
        app = request._app

        license = License.get_license(license_code)
        data, valid = app.verify_envato_license_code(license_code)

        # Check DB license exists or not?
        if valid and not license:
            # Create a license.
            license = License.objects.create(
                license_code=license_code,
                license_type=License.TYPES.REGULAR_LICENSE,
                checks=0,
                app=app,
                amount=float(0),
            )

        # Update license (force=False)
        # Get the license from database && update it (sync with Envato).
        if license and not license.force:
            app.update_license(license, data, valid)

        if license:
            # Update license checks.
            license.checks += 1
            license.save()

            # Create a domain if not exists or update it.
            try:
                domain = Domain.objects.get(host=host)
                domain.checks += 1
                domain.save()

            except Domain.DoesNotExist:
                # add a new one.
                domain = Domain.objects.create(host=host, checks=1, license=license)
                license.domains.add(domain)

            # Use DB license
            # print('> License status:', license.get_status_display())
            # print('> valid:', valid)

            # verify the license code.
            if app.is_valid_license(license, valid):
                result = {
                    "status": license.get_status_display().upper(),
                    "license_type": license.get_license_type_display().upper(),
                    "message": "This license code is valid",
                    "hash": os.urandom(20).hex(),
                }
                return JsonResponse(result)

            if license.status == License.STATUS.BANNED:
                result = {
                    "status": License.STATUS.BANNED.name,
                    "license_type": license.get_license_type_display().upper(),
                    "message": "Invalid License, probably has been blacklisted!, for more info please contact the support.",
                    "hash": os.urandom(20).hex(),
                }
                return JsonResponse(result)

        # Default response
        result = {
            "status": License.STATUS.INACTIVE.name,
            "message": "Invalid License, please ensure you've inserted a correct license code, or contact the support for help.",
            "hash": os.urandom(20).hex(),
        }

    return JsonResponse(result, status=403)


def is_up(request):
    return JsonResponse({"is_up": True})
