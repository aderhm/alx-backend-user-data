#!/usr/bin/env python3
""" Module: BasicAuth Class
"""

from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64
import binascii


class BasicAuth(Auth):
    """ Class BasicAuth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if not authorization_header or not isinstance(
                authorization_header, str
                ) or not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Returns the decoded value of a
        Base64 string base64_authorization_header
        """
        if base64_authorization_header and isinstance(
                base64_authorization_header, str):
            try:
                encode = base64_authorization_header.encode('utf-8')
                base = base64.b64decode(encode)
                return base.decode('utf-8')
            except binascii.Error:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Returns the user email and password from the Base64 decoded value
        """
        if (decoded_base64_authorization_header and isinstance(
                decoded_base64_authorization_header, str
                ) and ":" in decoded_base64_authorization_header):
            credentials = decoded_base64_authorization_header.split(":", 1)
            return (credentials[0], credentials[1])
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads current user
        """
        header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(header)
        decoded = self.decode_base64_authorization_header(b64_header)
        user_credentials = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(*user_credentials)
