from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils.translation import gettext_lazy as _

from . import views
from .models import Survey


class IsSurveyOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        assert isinstance(obj, Survey), (
            'Expected a Survey instance, got {} instead.'.format(type(obj))
        )

        return obj.owner == request.user


class ReadOnlyWhenSurveyActive(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):

        assert isinstance(obj, Survey), (
            'Expected a Survey instance, got {} instead.'.format(type(obj))
        )

        return obj.is_active and request.method in SAFE_METHODS


class IsParentSurveyOwner(BasePermission):
    """
    Only the owner of obj.survey can edit. Any authenticated users can create
    object (creation permission should be enforced by validators).
    """

    def has_permission(self, request, view):
        assert isinstance(view, views.NestedViewMixIn)
        return view.parent_instance.owner == request.user

    def has_object_permission(self, request, view, obj):
        return obj.survey.owner == request.user


class ReadOnlyWhenParentSurveyActive(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS and view.parent_instance.is_active


class CreateOnlyWhenParentSurveyActive(BasePermission):

    def has_permission(self, request, view):
        assert isinstance(view, views.NestedViewMixIn)
        # allow OPTIONS
        if request.method == 'OPTIONS':
            return True
        # allow POST
        return request.method == 'POST' and view.parent_instance.is_active
