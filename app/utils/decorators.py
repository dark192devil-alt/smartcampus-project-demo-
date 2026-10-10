from functools import wraps

from flask import abort
from flask_login import current_user, login_required


ALLOWED_ROLES = {"student", "faculty", "admin"}


def role_required(*roles):
    requested_roles = set(roles)
    invalid_roles = requested_roles - ALLOWED_ROLES
    if invalid_roles:
        raise ValueError(f"Unsupported role(s): {', '.join(sorted(invalid_roles))}")

    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped_view(*args, **kwargs):
            if current_user.role not in requested_roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped_view

    return decorator
