import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .common import verify_envato_license_code
from .models import License

ENVATO_TOKEN = os.getenv('ENVATO_TOKEN', None)


@csrf_exempt
def check_license(request):

    if request.method == 'POST':
        license_code = request.POST.get('license_code')
        host = request.POST.get('host')

        if license_code and ENVATO_TOKEN:
            # Get the license from database && update it (sync with Envato).
            data, valid = verify_envato_license_code(
                license_code, ENVATO_TOKEN)

            license_type = License.TYPES.REGULAR_LICENSE if str(data.get(
                'license')).lower() == 'regular license' else License.TYPES.EXTENDED_LICENSE

            try:
                license = License.objects.get(license_code=license_code)
                # update license (sync with Envato)
                license.status = License.STATUS.INACTIVE if not valid else license.status
                license.checks += 1
                license.license_type = license_type
                license.amount = float(data.get('amount'))
                license.save()

            except License.DoesNotExist:
                # create/register a new license (if envato license data exists)
                if valid:
                    license = License.objects.create(
                        license_code=license_code,
                        license_type=license_type,
                        checks=1,
                        amount=float(data.get('amount'))
                    )

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
                        'message': "Invalid License, probably has been blacklisted!",
                        'hash': os.urandom(20).hex()
                    }
                    return JsonResponse(result)

            result = {
                'status': License.STATUS.INACTIVE.name,
                'message': "This license code isn't valid",
                'hash': os.urandom(20).hex()
            }
            return JsonResponse(result)

    return JsonResponse({}, status=403)
