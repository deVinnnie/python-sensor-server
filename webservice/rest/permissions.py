from rest_framework import permissions
from pprint import pprint
from data.models import Gateway, Permission

# For Measurement entity. Only the owning gateway can update.
# Measurements cannot be deleted and cannot be changed, by either the gateway or a user.
# A gateway authenticates itself with an API-key. This API-key must be transmitted as an additional parameter
# with each request.
class IsGatewayOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        print("Hello World, this is the guard.")

        #pprint(vars(request))
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


class IsUserAllowed(permissions.BasePermission):
    """
    Does the user has the right 'permissions' to view/edit this entity?
    This is ambiguous since the permissions concept differs in meaning for this class and for the user of the system.
    'Having permission' means that the user has a sufficiently high role, or that he is assigned the entity id in a seperate table.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, object):
        entities = ['Measurement', 'Sensor', 'Gateway', 'Installation', 'Company']
        entity = object
        print(entity.sensor.gateway.installation.company)

        # sensor = getattr(entity, "sensor")
        # print(sensor.sensor_id)

        while True:
            entityName = type(entity).__name__
            index = entities.index(entityName) + 1
            if index >= len(entities):
                return False
            parentEntityName = entities[index]
            print(parentEntityName)

            parentEntity = getattr(entity, parentEntityName.lower())

            print(parentEntity)
            id = getattr(parentEntity, "{}_id".format(parentEntityName.lower()))
            print(id)

            permissions = Permission.objects.filter(identifier=id, entity=parentEntityName.lower())

            if len(permissions) >= 1:
                return True
            else:
                entity = parentEntity