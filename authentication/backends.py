from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrUsernameModelBackend(ModelBackend):
    """Authentication backend which allows users to authenticate using either
    their username or their email address.

    It defers to the default ModelBackend for permission checks.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get('email') or kwargs.get(UserModel.EMAIL_FIELD)

        # try to fetch by username first
        user = None
        if username:
            # if the username looks like an email, try to lookup by email
            if '@' in username:
                try:
                    user = UserModel.objects.filter(email__iexact=username).first()
                except Exception:
                    user = None

            # fallback to username lookup
            if user is None:
                try:
                    user = UserModel._default_manager.get_by_natural_key(username)
                except Exception:
                    user = None

        if user is not None and user.check_password(password):
            return user
        return None
