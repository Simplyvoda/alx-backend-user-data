#!/usr/bin/env python3
"""
Module for Authentication methods
"""
import bcrypt
from db import DB


def _hash_password(password: str) -> bytes:
    """
    Returns salted hash of input password
    """
    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialises the DB
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user in the DB
        if not already registered
        """
        try:
            # Check if user with email already exists
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")

            # Hash the password
            hashed_password = self._hash_password(password)

            # Save the user to the database
            user = User(email=email, hashed_password=hashed_password)
            self._db.add_user(user)

            return user
        except Exception as e:
            # Handle any unexpected exceptions
            raise RuntimeError(f"Failed to register user: {e}")
