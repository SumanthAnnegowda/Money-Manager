from django.conf import settings
from django.core.mail import send_mail
from os import urandom as generate_bytes
from hashlib import sha256
from datetime import timedelta
from django.template import loader
from django.core.exceptions import ValidationError

import re
import random
import binascii

EMAIL_REGEX_PATTERN=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
AUTH_TOKEN_CHAR_LENGTH = 128
TOKEN_PREFIX = 'Token '
TOKEN_TTL = timedelta(hours=6)
TOKEN_KEY_LENGTH = 255
MAXIMUM_TOKEN_PREFIX_LENGTH = 10
DIGEST_LENGTH = 255

def validate_email(username):
    if re.fullmatch(EMAIL_REGEX_PATTERN, username):
        return True
    return False

def generate_token():
    token = TOKEN_PREFIX + create_token_string()
    return token

def create_token_string():
    return binascii.hexlify(
        generate_bytes(int(AUTH_TOKEN_CHAR_LENGTH / 2))
    ).decode()

def make_hex_compatible(token: str) -> str:
    "We need to make sure the sent token is hex compatible which is not guaranteed when token prefix is used"
    return binascii.unhexlify(binascii.hexlify(bytes(token, 'utf-8')))

def hash_token(token: str) -> str:
    """
    Calculates the hash of the token.
    Token must contain an even number of hex digits or a binsacii.Error exception will be raised 
    """
    digest = sha256()
    digest.update(make_hex_compatible(token))
    return digest.hexdigest()
