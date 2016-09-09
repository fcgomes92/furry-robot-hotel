from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _
from logging import getLogger
from hotel_example import models
from passlib.hash import pbkdf2_sha256
import base64
import binascii

logger = getLogger(__name__)


def authenticate_token(token):
    try:
        uid = settings.TOKEN_MANAGER.parse_token(token=token).get('id')
        if not uid:
            return None
        else:
            return models.User.objects.get(id=uid)
    except Exception as e:
        logger.warning(e)
        return None


def authenticate_password(credentials):
    try:
        user = models.User.objects.get(email=credentials.get('username'))
        if user.password is not None:
            if pbkdf2_sha256.verify(credentials.get('password').encode(),
                                    user.password):
                return user
            else:
                return None
        else:
            return None
    except Exception as e:
        return None


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """
    HTTP_HEADER_ENCODING = 'iso-8859-1'
    text_type = str
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, text_type):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user and not isinstance(request.user, AnonymousUser)


class PasswordAuthentication(BaseAuthentication):
    www_authenticate_realm = 'api'

    def authenticate_credentials(self, email, password):
        credentials = {
            'username': email,
            'password': password
        }

        user = authenticate_password(credentials)

        if user is None:
            raise exceptions.AuthenticationFailed(
                _('Invalid username/password.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.'))

        return (user, None)

    def authenticate_header(self, request):
        return 'Basic realm="%s"' % self.www_authenticate_realm

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                'Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            auth_parts = base64.b64decode(auth[1]).decode(
                HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _(
                'Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)

        email, password = auth_parts[0], auth_parts[2]
        return self.authenticate_credentials(email, password)


class TokenAuthentication(BaseAuthentication):
    keyword = 'Token'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            msg = 'Invalid token header.'
            logger.error(msg=msg)
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            logger.error(msg=msg)
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            logger.error(msg=msg)
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            logger.error(msg=msg)
            raise exceptions.AuthenticationFailed(msg)

        user = authenticate_token(token)

        if not user:
            msg = 'Invalid token.'
            logger.error(msg=msg)
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'User inactive or deleted.'
            logger.error(msg=msg)
            raise exceptions.AuthenticationFailed(msg)
        return user, token
