import os

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .common import verify_envato_license_code
from .models import License, Domain, App
from .decorators import api_key_required

ENVATO_TOKEN = os.getenv('ENVATO_TOKEN', None)


@csrf_exempt
@api_key_required
def check_license(request):

    if request.method == 'POST':
        license_code = request.POST.get('license_code')
        host = request.POST.get('host')
        app = request._app

        if license_code:
            # Get the license from database && update it (sync with Envato).
            data, valid = app.verify_envato_license_code(license_code)

            license_type = License.TYPES.REGULAR_LICENSE if str(data.get(
                'license')).lower() == 'regular license' else License.TYPES.EXTENDED_LICENSE

            try:
                license = License.objects.get(license_code=license_code)
                # update license (sync with Envato)
                if license.app == app:
                    license.status = License.STATUS.INACTIVE if not valid else license.status
                    license.checks += 1
                    license.license_type = license_type
                    license.amount = float(data.get('amount'))
                    license.save()

                    # add a domain if not exists
                    try:
                        domain = Domain.objects.get(host=host)
                        domain.checks += 1
                        domain.save()

                    except Domain.DoesNotExist:
                        # add a new one.
                        Domain.objects.create(
                            host=host, checks=1, license=license)

            except License.DoesNotExist:
                # create/register a new license (if envato license data exists)
                if valid:
                    license = License.objects.create(
                        license_code=license_code,
                        license_type=license_type,
                        checks=1,
                        app=app,
                        amount=float(data.get('amount'))
                    )
                    # create a domain as well.
                    Domain.objects.create(host=host, checks=1, license=license)

            # verify the license code.
            if valid:
                if license.status == license.STATUS.ACTIVE:
                    result = {
                        'status': license.get_status_display().upper(),
                        'message': "This license code is valid",
                        'hash': os.urandom(20).hex()
                    }
                    return JsonResponse(result)

                if license.status == License.STATUS.BANNED:
                    result = {
                        'status': License.STATUS.BANNED.name,
                        'message': "Invalid License, probably has been blacklisted!, for more info please contact the support.",
                        'hash': os.urandom(20).hex()
                    }
                    return JsonResponse(result)

            result = {
                'status': License.STATUS.INACTIVE.name,
                'message': "Invalid License, please ensure you've inserted a correct license code, or contact the support for help.",
                'hash': os.urandom(20).hex()
            }
            return JsonResponse(result)

    return JsonResponse({}, status=403)


def is_up(request):
    return JsonResponse({
        'is_up': True
    })
