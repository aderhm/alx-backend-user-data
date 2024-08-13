#!/usr/bin/env python3
""" This module defines the `User` class as an ORM model using SQLAlchemy.

The `User` class maps to the `users` table in the database and provides an
abstraction for interacting with user data. It includes fields for storing
user credentials, session information, and password reset tokens.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """ Represents a user entity in the system.

    This class defines the structure of the `users` table in the database,
    which stores user-related data.

    Attributes:
    -----------
    id : int
        The unique identifier for the user (primary key).
    email : str
        The user's email address, which is required and must be unique.
    hashed_password : str
        The hashed version of the user's password, stored securely.
    session_id : str, optional
        The session ID associated with the user, used to track active sessions.
    reset_token : str, optional
        A token used for password reset functionality.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
