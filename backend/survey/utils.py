from django.conf import settings
import hashlib


def build_auto_salt(*args):
    new_salt = getattr(settings, "HASHID_FIELD_SALT", "") \
        + "|" + "|".join([str(v) for v in args])
    return hashlib.sha1(new_salt.encode("utf-8")).hexdigest()
