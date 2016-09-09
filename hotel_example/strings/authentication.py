from django.utils.translation import ugettext_lazy as _

INVALID_USERNAME_PASSWORD = _('Invalid username/password.')
USER_NOT_ACTIVE = _('User inactive or deleted.')

# HEADER CREDENTIALS
INVALID_HEADER = _('Invalid basic header. No credentials provided.')
INVALID_HEADER_SPACES = _(
    'Invalid basic header. Credentials string should not contain spaces.')
INVALID_HEADER_ENCODE = _(
    'Invalid basic header. Credentials not correctly base64 encoded.')

# HEADER TOKEN
INVALID_TOKEN_HEADER = _('Invalid token header.')
INVALID_TOKEN = _('Invalid token header. No credentials provided.')
INVALID_TOKEN_SPACES = _(
    'Invalid token header. Token string should not contain spaces.')
INVALID_TOKEN_CHARS = _(
    'Invalid token header. Token string should not contain invalid characters.')
