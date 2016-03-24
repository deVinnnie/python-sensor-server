from rest_framework import permissions
from pprint import pprint
from data.models import Gateway

# For Measurement entity. Only the owning gateway can update.
# Measurements cannot be deleted and cannot be changed, by either the gateway or a user.
# A gateway authenticates itself with an API-key. This API-key must be transmitted as an additional parameter
# with each request.
class IsGatewayOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        print("Hello World, this is the guard.")

        pprint(vars(request))
        # pprint (vars(view))
        if request.user.is_authenticated():
            return True
        else:
            gateway_id = request.parser_context['kwargs']['gateway_pk']
            gateway = Gateway.objects.get(pk=gateway_id)

            api_key = request.GET.get('api_key')

            if api_key == gateway.api_key:
                return True
            else:
                return False
