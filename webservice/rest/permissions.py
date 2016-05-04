from rest_framework import permissions
from pprint import pprint
from data.models import Gateway, Permission

# For Measurement entity. Only the owning gateway can update.
# Measurements cannot be deleted and cannot be changed, by either the gateway or a user.
# A gateway authenticates itself with an API-key. This API-key must be transmitted as an additional parameter
# for each request.
class IsGatewayOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        #print("Hello World, this is the guard.")

        #pprint(vars(request))
        # pprint (vars(view))
        if request.user.is_authenticated():
            return True
        else:
            # When accessing the gateway directly the pk is stored in 'pk'.
            # In all other cases it is in 'gateway_pk'.
            if 'gateway_pk' in request.parser_context['kwargs']:
                gateway_id = request.parser_context['kwargs']['gateway_pk']
            else:
                gateway_id = request.parser_context['kwargs']['pk']

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
        if request.user.is_superuser:
            # Superuser is allowed to do absolutly everything
            return True

        print(view.action)
        if view.action != 'list':
            pk = request.parser_context['kwargs']['pk']
            object = view.getQSet().get(pk=pk)
            pprint(vars(object))

            return self.has_object_permission(request, view, object)
        else:
            return False

    def has_object_permission(self, request, view, object):
        if request.user.is_superuser:
            # Superuser is allowed to do absolutly everything
            return True

        # Note: we don't do permissions on Measurement level, the lowest level should be sensor.
        entities = ['Measurement', 'Sensor', 'Gateway', 'Installation', 'Company']
        entity = object
        #   print(entity.sensor.gateway.installation.company)

        # Do a recursive search. Begin at the bottom of the hierarchy and check for permission.
        # If the user doesn't have permission at the current level, the level above is searched.
        # This is repeated until the top of the hiearchy is reached.
        while True:
            entityName = type(entity).__name__
            id = getattr(entity, "{}_id".format(entityName.lower()))

            # Check the permissions table.
            permissions = Permission.objects.filter(user=request.user.id,
                                                    identifier=id,
                                                    entity=entityName.lower()
            )

            if len(permissions) >= 1:
                return True
            else:
                index = entities.index(entityName)
                if index + 1 >= len(entities):
                    # End of hiearchy reached. I'm sorry you don't have permission.
                    return False

                parentEntityName = entities[index+1]
                parentEntity = getattr(entity, parentEntityName.lower())
                entity = parentEntity


