#!/usr/bin/env python3
"""
Module for Authentication methods
"""
import bcrypt
from uuid import uuid4
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union

from user import User


def _hash_password(password: str) -> bytes:
    """
    Returns salted hash of input password
    """
    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_pwd


def _generate_uuid() -> str:
    """
    returns uuid string
    """
    return str(uuid4())


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
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a users credential returns true if password is true
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """creates new session for user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Gets a user based on their session id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return User
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        updates current user session id to none
        """
        if user_id is None:
            return None

        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates reset token for user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a users password
        """
        try:
            user = user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hashed_password = _hash_password(password)
                self._db.update_user(
                        user.id,
                        hashed_password=hashed_password,
                        reset_token=None
                )
        except NoResultFound:
            raise ValueError()
