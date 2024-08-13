#!/usr/bin/env python3
""" Auth module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """ Hashes a password
    """
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(pw_bytes, salt)
    return hashed_pw
