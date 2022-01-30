from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _


class OwnedByRequestUser:

    requires_context = True

    def __call__(self, value, serializer_field):
        if value.owner != serializer_field.context['request'].user:
            raise PermissionDenied(
                _("You don't have permission to edit {}.").format(value)
            )
