#!/usr/bin/env python3
""" Module: Class Auth
"""

import os
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class Auth
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a path requires auth
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns auth header
        """
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user
        """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request
        """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
