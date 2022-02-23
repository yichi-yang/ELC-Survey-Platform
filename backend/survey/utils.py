from http.client import NOT_FOUND
from django.conf import settings
import hashlib
from rest_framework.exceptions import NotFound


def build_auto_salt(*args):
    new_salt = getattr(settings, "HASHID_FIELD_SALT", "") \
        + "|" + "|".join([str(v) for v in args])
    return hashlib.sha1(new_salt.encode("utf-8")).hexdigest()


def handle_invalid_hashid(resource_name=None):
    """
    A decorator that turns ValueErrors raised due to invalid hashids
    into NotFounds so they can be handled by DRF's exception handling logic.
    
    resource_name: the name of the potential offender to be used
    in error messages
    """
    def decorator(func):
        def wrapper(view, *args, **kwargs):
            try:
                return func(view, *args, **kwargs)
            except ValueError as e:
                # FIXME: a bit sketchy but works for now
                if str(e).endswith("value must be a positive integer or a valid Hashids string."):
                    detail = f'{resource_name} not found.' if resource_name else None
                    raise NotFound(detail=detail)
                else:
                    raise e
        return wrapper
    return decorator

def query_param_to_bool(s):
    """
    Returns True if s.lower() == 'true' and returns false if s.lower() == 'false'.
    Otherwise None is returned.
    """
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    return None
