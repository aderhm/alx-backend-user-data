#!/usr/bin/env python3
""" Auth module
"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Hashes a password
    """
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(pw_bytes, salt)
    return hashed_pw


def _generate_uuid() -> str:
    """ Generate UUIDs
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a new user
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate credentials
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            pw_bytes = password.encode('utf-8')
            return bcrypt.checkpw(pw_bytes, existing_user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Creates a session for a user
        """
        try:
            user = self._db.find_user_by(email=email)
            sid = _generate_uuid()
            self._db.update_user(user.id, session_id=sid)
            return sid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Find user by session id
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy user session
        """
        self._db.update_user(user_id, session_id=None)
        return None
