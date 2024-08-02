#!/usr/bin/env python3
"""Module: Encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks validity.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
